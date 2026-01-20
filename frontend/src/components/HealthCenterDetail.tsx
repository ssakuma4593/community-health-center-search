import ReactMarkdown from 'react-markdown';
import type { HealthCenter } from '../types';

interface HealthCenterDetailProps {
  center: HealthCenter | null;
  onClose: () => void;
}

export default function HealthCenterDetail({
  center,
  onClose,
}: HealthCenterDetailProps) {
  if (!center) return null;

  // Use OpenAI enriched data if available, otherwise fall back to original data
  const displayPhone = center.openai_phone || center.phone;
  const displayAddress = center.openai_address || 
    `${center.street_address_1}${center.street_address_2 ? `, ${center.street_address_2}` : ''}, ${center.city_town}, ${center.state} ${center.zipcode}`;
  
  const newPatientInstructions = center.openai_new_patient_md || 
    'Contact information is available above. Please call or visit the center for details on becoming a new patient.';
  
  const otherNotes = center.openai_other_notes_md;

  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>
        
        <h1>{center.name}</h1>
        
        <div className="detail-section">
          <h2>Contact Information</h2>
          <p><strong>Address:</strong> {displayAddress}</p>
          {displayPhone && <p><strong>Telephone:</strong> {displayPhone}</p>}
          {center.website && (
            <p>
              <strong>Website:</strong>{' '}
              <a href={center.website} target="_blank" rel="noopener noreferrer">
                {center.website}
              </a>
            </p>
          )}
        </div>

        {center.types && (
          <div className="detail-section">
            <h2>Services</h2>
            <p>{center.types}</p>
          </div>
        )}

        {center.distance !== undefined && (
          <div className="detail-section">
            <h2>Distance</h2>
            <p>{center.distance.toFixed(1)} miles away</p>
          </div>
        )}

        <div className="detail-section">
          <h2>How to Become a New Patient</h2>
          <div className="markdown-content">
            <ReactMarkdown>{newPatientInstructions}</ReactMarkdown>
          </div>
        </div>

        {otherNotes && (
          <div className="detail-section">
            <h2>Additional Notes</h2>
            <div className="markdown-content">
              <ReactMarkdown>{otherNotes}</ReactMarkdown>
            </div>
          </div>
        )}

        {center.openai_confidence && (
          <div className="detail-section metadata">
            <p className="metadata-text">
              <small>Information confidence: {center.openai_confidence}</small>
              {center.openai_last_checked_utc && (
                <small> • Last checked: {new Date(center.openai_last_checked_utc).toLocaleDateString()}</small>
              )}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
