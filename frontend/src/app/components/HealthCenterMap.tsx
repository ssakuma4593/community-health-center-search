"use client";

import { APIProvider, Map, Marker, InfoWindow } from '@vis.gl/react-google-maps';
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
  const [mapError, setMapError] = useState<string>('');
  
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
  
  if (mapError) {
    return (
      <div className="w-full h-[600px] bg-gray-100 rounded-lg flex items-center justify-center">
        <div className="text-center p-6">
          <p className="text-red-600 font-semibold mb-2">Map Loading Error</p>
          <p className="text-gray-600 text-sm">{mapError}</p>
          <div className="mt-4 text-xs text-gray-500 text-left max-w-md">
            <p className="font-semibold mb-2">Common fixes:</p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Enable "Maps JavaScript API" in Google Cloud Console</li>
              <li>Wait 2-3 minutes after enabling billing</li>
              <li>Check API key restrictions (allow localhost:3000)</li>
              <li>Verify billing is enabled on your project</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Filter health centers that have valid coordinates
  const centersWithCoordinates = healthCenters.filter(
    center => center.latitude && center.longitude
  );

  // Calculate default map center - use Massachusetts center
  // Massachusetts center coordinates for initial view
  const massachusettsCenter = { lat: 42.4072, lng: -71.3824 };
  
  const defaultCenter = centersWithCoordinates.length > 0
    ? {
        lat: centersWithCoordinates.reduce((sum, c) => sum + (c.latitude || 0), 0) / centersWithCoordinates.length,
        lng: centersWithCoordinates.reduce((sum, c) => sum + (c.longitude || 0), 0) / centersWithCoordinates.length,
      }
    : massachusettsCenter;
  
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
      <APIProvider 
        apiKey={apiKey}
        onLoad={() => console.log('Maps API loaded successfully')}
        onError={(error) => {
          console.error('Maps API error:', error);
          setMapError(error.message || 'Failed to load Google Maps');
        }}
      >
        <Map
          center={displayCenter}
          zoom={mapZoom}
          gestureHandling="greedy"
          disableDefaultUI={false}
          mapTypeId="roadmap"
        >
          {centersWithCoordinates.map((healthCenter, index) => {
            const highlighted = isHighlighted(healthCenter);
            
            return (
              <Marker
                key={index}
                position={{ lat: healthCenter.latitude!, lng: healthCenter.longitude! }}
                onClick={() => setSelectedCenter(healthCenter)}
                title={healthCenter.name}
                label={highlighted ? { 
                  text: '●', 
                  color: '#ffffff',
                  fontSize: '20px',
                  fontWeight: 'bold'
                } : undefined}
              />
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

