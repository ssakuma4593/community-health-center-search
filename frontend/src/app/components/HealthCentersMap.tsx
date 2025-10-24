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

export default function HealthCentersMap({ healthCenters, zipcode }: HealthCentersMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mapRef.current || healthCenters.length === 0) return;

    // Clear previous map
    mapRef.current.innerHTML = '';

    // Create map container with OpenStreetMap
    const mapContainer = document.createElement('div');
    mapContainer.style.width = '100%';
    mapContainer.style.height = '400px';
    mapContainer.style.borderRadius = '8px';
    mapContainer.style.border = '1px solid #e5e7eb';
    mapContainer.style.overflow = 'hidden';
    mapContainer.style.position = 'relative';

    // Create iframe for OpenStreetMap
    const mapFrame = document.createElement('iframe');
    mapFrame.style.width = '100%';
    mapFrame.style.height = '100%';
    mapFrame.style.border = 'none';
    mapFrame.style.borderRadius = '8px';
    
    // Create a simple map URL with the zipcode center
    // This is a basic implementation - in production you'd want to geocode the addresses
    const mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=-71.5,42.0,-70.5,42.5&layer=mapnik&marker=42.3601,-71.0589`;
    mapFrame.src = mapUrl;
    mapFrame.title = `Health Centers Map for ${zipcode}`;

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
    overlay.textContent = `${healthCenters.length} Health Centers in ${zipcode}`;

    mapContainer.appendChild(overlay);

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
    listTitle.style.margin = '0 0 12px 0';

    listContainer.appendChild(listTitle);

    healthCenters.forEach((center, index) => {
      const centerDiv = document.createElement('div');
      centerDiv.style.padding = '12px';
      centerDiv.style.borderBottom = index < healthCenters.length - 1 ? '1px solid #f3f4f6' : 'none';
      centerDiv.style.display = 'flex';
      centerDiv.style.alignItems = 'flex-start';
      centerDiv.style.gap = '12px';

      // Add marker icon
      const markerIcon = document.createElement('div');
      markerIcon.innerHTML = `
        <svg width="16" height="16" fill="#ef4444" viewBox="0 0 24 24">
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
        Map View - {zipcode}
      </h2>
      <div ref={mapRef} className="w-full" />
    </div>
  );
}
