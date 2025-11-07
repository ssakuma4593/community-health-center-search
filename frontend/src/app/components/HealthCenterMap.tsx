"use client";

import { APIProvider, Map, AdvancedMarker, InfoWindow, Pin } from '@vis.gl/react-google-maps';
import { useState, useEffect } from 'react';

interface HealthCenter {
  name: string;
  street_address_1: string;
  street_address_2?: string;
  city_town: string;
  state: string;
  zipcode: string;
  phone: string;
  types: string;
  website?: string;
  latitude?: number;
  longitude?: number;
}

interface HealthCenterMapProps {
  healthCenters: HealthCenter[];
  highlightedCenters?: HealthCenter[];
  center?: { lat: number; lng: number } | null;
  zoom?: number;
}

export default function HealthCenterMap({ 
  healthCenters,
  highlightedCenters = [],
  center = null,
  zoom = 8
}: HealthCenterMapProps) {
  const [selectedCenter, setSelectedCenter] = useState<HealthCenter | null>(null);
  const [mapCenter, setMapCenter] = useState<{ lat: number; lng: number } | null>(center);
  const [mapZoom, setMapZoom] = useState(zoom);
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';
  
  // Update map when center prop changes
  useEffect(() => {
    if (center) {
      setMapCenter(center);
      setMapZoom(zoom);
    }
  }, [center, zoom]);

  if (!apiKey) {
    return (
      <div className="w-full h-[600px] bg-gray-100 rounded-lg flex items-center justify-center">
        <div className="text-center p-6">
          <p className="text-red-600 font-semibold mb-2">Google Maps API Key Required</p>
          <p className="text-gray-600 text-sm">
            Please add NEXT_PUBLIC_GOOGLE_MAPS_API_KEY to your .env.local file
          </p>
        </div>
      </div>
    );
  }

  // Filter health centers that have valid coordinates
  const centersWithCoordinates = healthCenters.filter(
    center => center.latitude && center.longitude
  );

  // Calculate default map center based on health centers if no center is set
  const defaultCenter = centersWithCoordinates.length > 0
    ? {
        lat: centersWithCoordinates.reduce((sum, c) => sum + (c.latitude || 0), 0) / centersWithCoordinates.length,
        lng: centersWithCoordinates.reduce((sum, c) => sum + (c.longitude || 0), 0) / centersWithCoordinates.length,
      }
    : { lat: 42.3601, lng: -71.0589 }; // Default to Boston
  
  const displayCenter = mapCenter || defaultCenter;
  
  // Check if a health center is highlighted
  const isHighlighted = (healthCenter: HealthCenter) => {
    if (highlightedCenters.length === 0) return false;
    return highlightedCenters.some(hc => 
      hc.name === healthCenter.name && 
      hc.street_address_1 === healthCenter.street_address_1
    );
  };

  return (
    <div className="w-full h-[600px] rounded-lg overflow-hidden shadow-lg">
      <APIProvider apiKey={apiKey}>
        <Map
          center={displayCenter}
          zoom={mapZoom}
          mapId="health-centers-map"
          gestureHandling="greedy"
          disableDefaultUI={false}
        >
          {centersWithCoordinates.map((healthCenter, index) => {
            const highlighted = isHighlighted(healthCenter);
            return (
              <AdvancedMarker
                key={index}
                position={{ lat: healthCenter.latitude!, lng: healthCenter.longitude! }}
                onClick={() => setSelectedCenter(healthCenter)}
              >
                <Pin
                  background={highlighted ? "#dc2626" : "#2563eb"}
                  borderColor={highlighted ? "#991b1b" : "#1e40af"}
                  glyphColor="#ffffff"
                  scale={highlighted ? 1.2 : 1}
                />
              </AdvancedMarker>
            );
          })}

          {selectedCenter && selectedCenter.latitude && selectedCenter.longitude && (
            <InfoWindow
              position={{ lat: selectedCenter.latitude, lng: selectedCenter.longitude }}
              onCloseClick={() => setSelectedCenter(null)}
            >
              <div className="p-2 max-w-xs">
                <h3 className="font-semibold text-gray-900 mb-2">{selectedCenter.name}</h3>
                <div className="space-y-1 text-sm text-gray-600">
                  <p>
                    {selectedCenter.street_address_1}
                    {selectedCenter.street_address_2 && `, ${selectedCenter.street_address_2}`}
                  </p>
                  <p>{selectedCenter.city_town}, {selectedCenter.state} {selectedCenter.zipcode}</p>
                  <p className="font-medium">{selectedCenter.phone}</p>
                  {selectedCenter.types && (
                    <p className="text-blue-600">{selectedCenter.types}</p>
                  )}
                  {selectedCenter.website && (
                    <a
                      href={selectedCenter.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 underline block"
                    >
                      Visit Website
                    </a>
                  )}
                </div>
              </div>
            </InfoWindow>
          )}
        </Map>
      </APIProvider>
    </div>
  );
}

