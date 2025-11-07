"use client";

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

interface HealthCenterListProps {
  healthCenters: HealthCenter[];
  onCenterClick?: (center: HealthCenter) => void;
}

export default function HealthCenterList({ healthCenters, onCenterClick }: HealthCenterListProps) {
  return (
    <div className="space-y-4">
      {healthCenters.map((center, index) => (
        <div
          key={index}
          className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => onCenterClick?.(center)}
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {center.name}
          </h3>
          <div className="space-y-1 text-sm text-gray-600">
            <p>
              <strong>Address:</strong> {center.street_address_1}
              {center.street_address_2 && `, ${center.street_address_2}`}
              {`, ${center.city_town}, ${center.state} ${center.zipcode}`}
            </p>
            <p><strong>Phone:</strong> {center.phone}</p>
            {center.types && <p><strong>Services:</strong> {center.types}</p>}
            {center.website && (
              <p>
                <strong>Website:</strong>{" "}
                <a
                  href={center.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline"
                  onClick={(e) => e.stopPropagation()}
                >
                  {center.website}
                </a>
              </p>
            )}
            {center.latitude && center.longitude && (
              <p className="text-xs text-gray-500">
                📍 Coordinates: {center.latitude.toFixed(6)}, {center.longitude.toFixed(6)}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

