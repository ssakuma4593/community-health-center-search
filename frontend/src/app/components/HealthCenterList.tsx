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
  // Call data fields
  accepting_new_patients?: string;
  has_waiting_list?: string;
  waiting_list_availability_date?: string;
  languages_supported?: string;
  call_notes?: string;
  last_called_date?: string;
  call_status?: string;
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
          
          {/* Call Information Section */}
          {(center.accepting_new_patients || center.has_waiting_list || center.languages_supported || center.last_called_date) && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <h4 className="text-sm font-semibold text-gray-900 mb-2">📞 Call Information</h4>
              <div className="space-y-2 text-sm">
                {center.accepting_new_patients && (
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-700">Accepting New Patients:</span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      center.accepting_new_patients.toLowerCase() === 'yes' 
                        ? 'bg-green-100 text-green-800' 
                        : center.accepting_new_patients.toLowerCase() === 'no'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {center.accepting_new_patients}
                    </span>
                  </div>
                )}
                {center.has_waiting_list && (
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-700">Waiting List:</span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      center.has_waiting_list.toLowerCase() === 'yes' 
                        ? 'bg-yellow-100 text-yellow-800' 
                        : center.has_waiting_list.toLowerCase() === 'no'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {center.has_waiting_list}
                    </span>
                  </div>
                )}
                {center.waiting_list_availability_date && center.waiting_list_availability_date !== 'N/A' && (
                  <div>
                    <span className="font-medium text-gray-700">Expected Availability: </span>
                    <span className="text-gray-600">{center.waiting_list_availability_date}</span>
                  </div>
                )}
                {center.languages_supported && (
                  <div>
                    <span className="font-medium text-gray-700">Languages Supported: </span>
                    <span className="text-gray-600">{center.languages_supported}</span>
                  </div>
                )}
                {center.call_notes && (
                  <div>
                    <span className="font-medium text-gray-700">Notes: </span>
                    <span className="text-gray-600 italic">{center.call_notes}</span>
                  </div>
                )}
                {center.last_called_date && (
                  <p className="text-xs text-gray-500 mt-2">
                    Last called: {new Date(center.last_called_date).toLocaleDateString()}
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

