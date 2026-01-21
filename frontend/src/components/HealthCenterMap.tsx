import { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { HealthCenter } from '../types';

// Fix for default marker icons in Leaflet with Vite
// Use direct paths since Vite handles these assets
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const DefaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

interface MapControllerProps {
  centers: HealthCenter[];
  selectedCenter: HealthCenter | null;
}

function MapController({ centers, selectedCenter }: MapControllerProps) {
  const map = useMap();

  useEffect(() => {
    if (centers.length === 0) return;

    if (selectedCenter) {
      map.setView([selectedCenter.latitude, selectedCenter.longitude], 13);
    } else {
      const bounds = L.latLngBounds(
        centers.map((c) => [c.latitude, c.longitude] as [number, number])
      );
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [centers, selectedCenter, map]);

  return null;
}

interface HealthCenterMapProps {
  centers: HealthCenter[];
  selectedCenter: HealthCenter | null;
  onCenterClick: (center: HealthCenter) => void;
}

export default function HealthCenterMap({
  centers,
  selectedCenter,
  onCenterClick,
}: HealthCenterMapProps) {

  if (centers.length === 0) {
    return (
      <div className="map-container empty">
        <p>No centers found. Try a different zipcode.</p>
      </div>
    );
  }

  // Default center (Massachusetts)
  const defaultCenter: [number, number] = [42.3601, -71.0589];
  const defaultZoom = 8;

  return (
    <div className="map-container">
      <MapContainer
        key={`map-${centers.length}-${selectedCenter?.name || 'none'}`}
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapController centers={centers} selectedCenter={selectedCenter} />
        {centers.map((center, index) => (
          <Marker
            key={index}
            position={[center.latitude, center.longitude]}
            eventHandlers={{
              click: () => onCenterClick(center),
            }}
          >
            <Popup>
              <div>
                <h3>{center.name}</h3>
                <p>
                  {center.street_address_1}
                  {center.street_address_2 && `, ${center.street_address_2}`}
                  <br />
                  {center.city_town}, {center.state} {center.zipcode}
                </p>
                {center.distance !== undefined && (
                  <p className="distance">{center.distance.toFixed(1)} miles away</p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
