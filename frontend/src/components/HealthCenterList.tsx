import type { HealthCenter } from '../types';

interface HealthCenterListProps {
  centers: HealthCenter[];
  selectedCenter: HealthCenter | null;
  onCenterClick: (center: HealthCenter) => void;
  isFiltered?: boolean;
}

export default function HealthCenterList({
  centers,
  selectedCenter,
  onCenterClick,
  isFiltered = false,
}: HealthCenterListProps) {
  if (centers.length === 0) {
    return (
      <div className="center-list empty">
        <p>No centers found within the selected radius. Try a different zipcode or expand the radius.</p>
      </div>
    );
  }

  return (
    <div className="center-list">
      <h2>
        {isFiltered 
          ? `Found ${centers.length} center${centers.length !== 1 ? 's' : ''}`
          : `All Health Centers (${centers.length} total)`}
      </h2>
      <div className="center-cards">
        {centers.map((center, index) => (
          <div
            key={index}
            className={`center-card ${selectedCenter === center ? 'selected' : ''}`}
            onClick={() => onCenterClick(center)}
          >
            <h3>{center.name}</h3>
            <div className="center-info">
              <p className="address">
                {center.street_address_1}
                {center.street_address_2 && `, ${center.street_address_2}`}
                <br />
                {center.city_town}, {center.state} {center.zipcode}
              </p>
              {center.phone && (
                <p className="phone">
                  <strong>Phone:</strong>{' '}
                  <a 
                    href={`tel:${center.phone.replace(/\D/g, '')}`}
                    className="phone-link"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {center.phone}
                  </a>
                </p>
              )}
              {(center.all_services || center.final_types || center.openai_types || center.types) && (
                <p className="types">
                  <strong>Services:</strong> {center.all_services || center.final_types || center.openai_types || center.types}
                </p>
              )}
              {center.distance !== undefined && (
                <p className="distance">
                  <strong>Distance:</strong> {center.distance.toFixed(1)} miles
                </p>
              )}
            </div>
            <button className="view-details-btn">View Details</button>
          </div>
        ))}
      </div>
    </div>
  );
}
