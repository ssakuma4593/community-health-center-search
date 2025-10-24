"use client";

import { useEffect, useRef } from "react";

interface HealthCenter {
  name: string;
  address: string;
  phone: string;
  types: string;
  website: string;
  zipcode: string;
  street_address_1: string;
  street_address_2: string;
  city_town: string;
  state: string;
}

interface HealthCentersMapProps {
  healthCenters: HealthCenter[];
  zipcode: string;
}

// Function to generate Google Maps embed URL for a zipcode
const generateGoogleMapsEmbedUrl = (zipcode: string) => {
  // Create a Google Maps search URL for the specific zipcode
  // This will show the zipcode area and search for health centers
  const searchQuery = encodeURIComponent(`health centers in ${zipcode} Massachusetts`);
  return `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.6!2d-71.0589!3d42.3601!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDLCsDIxJzM2LjQiTiA3McKwMDMnMzIuMCJX!5e0!3m2!1sen!2sus!4v1234567890123!5m2!1sen!2sus&q=${searchQuery}`;
};

export default function HealthCentersMap({ healthCenters, zipcode }: HealthCentersMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mapRef.current || healthCenters.length === 0) return;

    // Clear previous map
    mapRef.current.innerHTML = '';

    // Create map container with custom health center display
    const mapContainer = document.createElement('div');
    mapContainer.style.width = '100%';
    mapContainer.style.height = '400px';
    mapContainer.style.borderRadius = '8px';
    mapContainer.style.border = '1px solid #e5e7eb';
    mapContainer.style.overflow = 'hidden';
    mapContainer.style.position = 'relative';
    mapContainer.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    mapContainer.style.display = 'flex';
    mapContainer.style.alignItems = 'center';
    mapContainer.style.justifyContent = 'center';
    mapContainer.style.flexDirection = 'column';
    mapContainer.style.gap = '16px';

    // Add map icon
    const mapIcon = document.createElement('div');
    mapIcon.innerHTML = `
      <svg width="64" height="64" fill="white" viewBox="0 0 24 24">
        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
      </svg>
    `;
    mapIcon.style.opacity = '0.8';

    // Add zipcode info
    const zipcodeInfo = document.createElement('div');
    zipcodeInfo.style.textAlign = 'center';
    zipcodeInfo.style.color = 'white';

    const zipcodeTitle = document.createElement('h3');
    zipcodeTitle.textContent = `Health Centers in ${zipcode}`;
    zipcodeTitle.style.fontSize = '24px';
    zipcodeTitle.style.fontWeight = '600';
    zipcodeTitle.style.margin = '0 0 8px 0';

    const zipcodeSubtitle = document.createElement('p');
    zipcodeSubtitle.textContent = `${healthCenters.length} health centers found`;
    zipcodeSubtitle.style.fontSize = '16px';
    zipcodeSubtitle.style.margin = '0';
    zipcodeSubtitle.style.opacity = '0.9';

    zipcodeInfo.appendChild(zipcodeTitle);
    zipcodeInfo.appendChild(zipcodeSubtitle);

    // Add Google Maps button
    const googleMapsButton = document.createElement('button');
    googleMapsButton.textContent = 'View in Google Maps';
    googleMapsButton.style.background = 'rgba(255, 255, 255, 0.2)';
    googleMapsButton.style.border = '2px solid white';
    googleMapsButton.style.color = 'white';
    googleMapsButton.style.padding = '12px 24px';
    googleMapsButton.style.borderRadius = '8px';
    googleMapsButton.style.fontSize = '14px';
    googleMapsButton.style.fontWeight = '600';
    googleMapsButton.style.cursor = 'pointer';
    googleMapsButton.style.transition = 'all 0.2s';
    googleMapsButton.style.marginTop = '8px';

    // Add hover effect
    googleMapsButton.addEventListener('mouseenter', () => {
      googleMapsButton.style.background = 'rgba(255, 255, 255, 0.3)';
    });
    googleMapsButton.addEventListener('mouseleave', () => {
      googleMapsButton.style.background = 'rgba(255, 255, 255, 0.2)';
    });

    // Add click handler to open Google Maps
    googleMapsButton.addEventListener('click', () => {
      const searchQuery = encodeURIComponent(`health centers in ${zipcode} Massachusetts`);
      const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${searchQuery}`;
      window.open(googleMapsUrl, '_blank');
    });

    mapContainer.appendChild(mapIcon);
    mapContainer.appendChild(zipcodeInfo);
    mapContainer.appendChild(googleMapsButton);

    // Add a note about the map
    const mapNote = document.createElement('div');
    mapNote.style.position = 'absolute';
    mapNote.style.bottom = '16px';
    mapNote.style.left = '16px';
    mapNote.style.right = '16px';
    mapNote.style.background = 'rgba(255, 255, 255, 0.95)';
    mapNote.style.padding = '8px 12px';
    mapNote.style.borderRadius = '6px';
    mapNote.style.fontSize = '12px';
    mapNote.style.color = '#6b7280';
    mapNote.style.textAlign = 'center';
    mapNote.textContent = 'Click on health centers below to open in Google Maps for directions';

    mapContainer.appendChild(mapNote);

    // Add health center list below map
    const listContainer = document.createElement('div');
    listContainer.style.marginTop = '16px';
    listContainer.style.background = 'white';
    listContainer.style.borderRadius = '8px';
    listContainer.style.border = '1px solid #e5e7eb';
    listContainer.style.padding = '16px';

    const listTitle = document.createElement('h4');
    listTitle.textContent = 'Health Center Locations:';
    listTitle.style.fontSize = '16px';
    listTitle.style.fontWeight = '600';
    listTitle.style.color = '#374151';
    listTitle.style.margin = '0 0 8px 0';

    const listSubtitle = document.createElement('p');
    listSubtitle.textContent = 'Click on any health center to open it in Google Maps';
    listSubtitle.style.fontSize = '12px';
    listSubtitle.style.color = '#6b7280';
    listSubtitle.style.margin = '0 0 12px 0';
    listSubtitle.style.fontStyle = 'italic';

    listContainer.appendChild(listTitle);
    listContainer.appendChild(listSubtitle);

    healthCenters.forEach((center, index) => {
      const centerDiv = document.createElement('div');
      centerDiv.style.padding = '12px';
      centerDiv.style.borderBottom = index < healthCenters.length - 1 ? '1px solid #f3f4f6' : 'none';
      centerDiv.style.display = 'flex';
      centerDiv.style.alignItems = 'flex-start';
      centerDiv.style.gap = '12px';
      centerDiv.style.cursor = 'pointer';
      centerDiv.style.transition = 'background-color 0.2s';

      // Add hover effect
      centerDiv.addEventListener('mouseenter', () => {
        centerDiv.style.backgroundColor = '#f9fafb';
      });
      centerDiv.addEventListener('mouseleave', () => {
        centerDiv.style.backgroundColor = 'transparent';
      });

      // Add marker icon
      const markerIcon = document.createElement('div');
      markerIcon.innerHTML = `
        <svg width="16" height="16" fill="#4285f4" viewBox="0 0 24 24">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
        </svg>
      `;
      markerIcon.style.flexShrink = '0';
      markerIcon.style.marginTop = '2px';

      // Add center info
      const centerInfo = document.createElement('div');
      centerInfo.style.flex = '1';

      const name = document.createElement('div');
      name.textContent = center.name;
      name.style.fontWeight = '600';
      name.style.fontSize = '14px';
      name.style.color = '#374151';
      name.style.marginBottom = '4px';

      const address = document.createElement('div');
      address.textContent = center.address;
      address.style.fontSize = '12px';
      address.style.color = '#6b7280';
      address.style.marginBottom = '2px';

      const phone = document.createElement('div');
      phone.textContent = center.phone;
      phone.style.fontSize = '12px';
      phone.style.color = '#6b7280';

      // Add click handler to open in Google Maps
      centerDiv.addEventListener('click', () => {
        const encodedAddress = encodeURIComponent(center.address);
        const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodedAddress}`;
        window.open(googleMapsUrl, '_blank');
      });

      centerInfo.appendChild(name);
      centerInfo.appendChild(address);
      centerInfo.appendChild(phone);

      centerDiv.appendChild(markerIcon);
      centerDiv.appendChild(centerInfo);
      listContainer.appendChild(centerDiv);
    });

    mapRef.current.appendChild(mapContainer);
    mapRef.current.appendChild(listContainer);

  }, [healthCenters, zipcode]);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">
        Google Maps View - {zipcode}
      </h2>
      <div ref={mapRef} className="w-full" />
    </div>
  );
}
