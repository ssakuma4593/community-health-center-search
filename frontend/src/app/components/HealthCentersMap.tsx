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
  // For Massachusetts zipcodes, we'll use a general Massachusetts map
  // This is a standard Google Maps embed that doesn't require API key
  const massachusettsMapUrl = `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.6!2d-71.0589!3d42.3601!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDLCsDIxJzM2LjQiTiA3McKwMDMnMzIuMCJX!5e0!3m2!1sen!2sus!4v1234567890123!5m2!1sen!2sus`;
  
  // For now, we'll use the general Massachusetts map
  // In a production app, you could use a geocoding service to get coordinates for the zipcode
  return massachusettsMapUrl;
};

export default function HealthCentersMap({ healthCenters, zipcode }: HealthCentersMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mapRef.current || healthCenters.length === 0) return;

    // Clear previous map
    mapRef.current.innerHTML = '';

    // Create map container with Google Maps
    const mapContainer = document.createElement('div');
    mapContainer.style.width = '100%';
    mapContainer.style.height = '400px';
    mapContainer.style.borderRadius = '8px';
    mapContainer.style.border = '1px solid #e5e7eb';
    mapContainer.style.overflow = 'hidden';
    mapContainer.style.position = 'relative';

    // Create iframe for Google Maps
    const mapFrame = document.createElement('iframe');
    mapFrame.style.width = '100%';
    mapFrame.style.height = '100%';
    mapFrame.style.border = 'none';
    mapFrame.style.borderRadius = '8px';
    
    // Generate the Google Maps embed URL
    const mapUrl = generateGoogleMapsEmbedUrl(zipcode);
    
    mapFrame.src = mapUrl;
    mapFrame.title = `Health Centers Map for ${zipcode}`;
    mapFrame.allowFullscreen = true;
    mapFrame.loading = 'lazy';

    mapContainer.appendChild(mapFrame);

    // Add overlay with health center count
    const overlay = document.createElement('div');
    overlay.style.position = 'absolute';
    overlay.style.top = '16px';
    overlay.style.left = '16px';
    overlay.style.background = 'rgba(255, 255, 255, 0.95)';
    overlay.style.padding = '12px 16px';
    overlay.style.borderRadius = '8px';
    overlay.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    overlay.style.fontSize = '14px';
    overlay.style.fontWeight = '600';
    overlay.style.color = '#374151';
    overlay.style.zIndex = '1000';
    overlay.textContent = `${healthCenters.length} Health Centers in ${zipcode}`;

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

    mapContainer.appendChild(overlay);
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
