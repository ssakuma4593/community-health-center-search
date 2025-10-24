#!/usr/bin/env python3
"""
Targeted Structure Scraper for Community Health Centers
Specifically targets the wpgb-card structure found in the HTML
"""

import json
import csv
import time
import re
from typing import List, Dict, Optional
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TargetedStructureScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.centers = []
        
    def setup_driver(self):
        """Set up Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            return False
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def extract_health_centers_from_page(self) -> List[Dict]:
        """Extract health centers using the specific wpgb-card structure"""
        centers = []
        
        try:
            # Wait for content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for the specific health center cards to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".wpgb-card"))
            )
            
            # Additional wait for dynamic content
            time.sleep(3)
            
            # Get page source and parse
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all health center cards
            health_cards = soup.find_all('article', class_='wpgb-card')
            logger.info(f"Found {len(health_cards)} health center cards on this page")
            
            for card in health_cards:
                center_info = self.parse_health_center_card(card)
                if center_info:
                    centers.append(center_info)
                    logger.info(f"Extracted: {center_info['name']}")
            
            logger.info(f"Found {len(centers)} valid health centers on this page")
            return centers
            
        except Exception as e:
            logger.error(f"Error extracting centers from page: {e}")
            return []
    
    def parse_health_center_card(self, card) -> Optional[Dict]:
        """Parse a health center card using the specific structure"""
        center_info = {
            'name': '',
            'address': '',
            'phone': '',
            'types': [],
            'website': ''
        }
        
        try:
            # Extract name from h3 element
            name_elem = card.find('h3')
            if name_elem:
                center_info['name'] = name_elem.get_text().strip()
            
            # Extract service types from term spans
            term_spans = card.find_all('span', class_='wpgb-block-term')
            for span in term_spans:
                service_type = span.get_text().strip()
                if service_type:
                    center_info['types'].append(service_type)
            
            # Extract address from address blocks
            address_blocks = card.find_all('div', class_='address-acf')
            address_parts = []
            for block in address_blocks:
                text = block.get_text().strip()
                if text and not text.startswith('('):  # Skip phone numbers
                    address_parts.append(text)
            
            if address_parts:
                center_info['address'] = ' '.join(address_parts)
            
            # Extract phone number
            phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            card_text = card.get_text()
            phone_match = re.search(phone_pattern, card_text)
            if phone_match:
                center_info['phone'] = phone_match.group().strip()
            
            # Extract website link
            website_link = card.find('a', href=True)
            if website_link:
                href = website_link.get('href')
                if href and not href.startswith('#') and 'massleague.org' not in href:
                    center_info['website'] = href
            
            # Only return if we have essential info
            if center_info['name'] and center_info['address'] and center_info['phone']:
                return center_info
                
        except Exception as e:
            logger.error(f"Error parsing health center card: {e}")
        
        return None
    
    def find_next_button(self) -> bool:
        """Find and click the next button"""
        try:
            # Look for pagination elements
            next_selectors = [
                "a[href*='next']",
                "a:contains('Next')",
                "a:contains('>>')",
                ".pagination a:contains('Next')",
                ".wpgb-pagination a:contains('Next')"
            ]
            
            for selector in next_selectors:
                try:
                    if ':contains(' in selector:
                        xpath = f"//a[contains(text(), 'Next')] | //a[contains(text(), '>>')]"
                        elements = self.driver.find_elements(By.XPATH, xpath)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                logger.info(f"Found next button with selector: {selector}")
                                element.click()
                                time.sleep(3)  # Wait for page to load
                                return True
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            logger.warning("No next button found")
            return False
            
        except Exception as e:
            logger.error(f"Error finding next button: {e}")
            return False
    
    def scrape_with_pagination(self) -> List[Dict]:
        """Scrape all pages by clicking through pagination"""
        if not self.setup_driver():
            logger.error("Failed to setup WebDriver")
            return []
        
        all_centers = []
        page_num = 1
        
        try:
            # Navigate to the first page
            url = "https://www.massleague.org/public-resources/about-community-health-centers/find-a-community-health-center/"
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for initial page load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(5)  # Wait for JavaScript to load content
            
            while True:
                logger.info(f"Scraping page {page_num}")
                
                # Extract centers from current page
                page_centers = self.extract_health_centers_from_page()
                all_centers.extend(page_centers)
                
                logger.info(f"Found {len(page_centers)} centers on page {page_num}")
                logger.info(f"Total centers so far: {len(all_centers)}")
                
                # Try to find and click next button
                if not self.find_next_button():
                    logger.info("No more pages found, stopping")
                    break
                
                page_num += 1
                
                # Safety check to prevent infinite loops
                if page_num > 20:
                    logger.warning("Reached maximum page limit (20), stopping")
                    break
                
                # Wait for new page to load
                time.sleep(3)
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
        finally:
            self.close_driver()
        
        # Remove duplicates
        seen = set()
        unique_centers = []
        for center in all_centers:
            key = (center['name'], center['address'])
            if key not in seen:
                seen.add(key)
                unique_centers.append(center)
        
        logger.info(f"Total unique centers found: {len(unique_centers)}")
        return unique_centers
    
    def save_to_json(self, filename: str = "community_health_centers_targeted.json"):
        """Save to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.centers, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {filename}")
    
    def save_to_csv(self, filename: str = "community_health_centers_targeted.csv"):
        """Save to CSV"""
        if not self.centers:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'address', 'phone', 'types', 'website'])
            writer.writeheader()
            for center in self.centers:
                center_copy = center.copy()
                center_copy['types'] = ', '.join(center['types'])
                writer.writerow(center_copy)
        logger.info(f"Data saved to {filename}")
    
    def run(self):
        """Main method to run the targeted structure scraper"""
        logger.info("Starting Targeted Structure Community Health Center scraper...")
        logger.info("This scraper targets the specific wpgb-card structure")
        
        self.centers = self.scrape_with_pagination()
        
        if self.centers:
            self.save_to_json()
            self.save_to_csv()
            logger.info(f"Targeted structure scraping completed! Found {len(self.centers)} community health centers.")
        else:
            logger.warning("No centers found.")
        
        return self.centers

def main():
    """Main function"""
    scraper = TargetedStructureScraper(headless=True)
    centers = scraper.run()
    
    print(f"\n=== TARGETED STRUCTURE SCRAPING SUMMARY ===")
    print(f"Total centers found: {len(centers)}")
    
    if centers:
        print(f"\n📋 Sample data:")
        for i, center in enumerate(centers[:5]):
            print(f"\n  Center {i+1}:")
            print(f"    Name: {center['name']}")
            print(f"    Address: {center['address']}")
            print(f"    Phone: {center['phone']}")
            print(f"    Types: {', '.join(center['types'])}")
            print(f"    Website: {center['website']}")
    else:
        print("\n⚠️  No centers found. Check ChromeDriver installation.")

if __name__ == "__main__":
    main()
