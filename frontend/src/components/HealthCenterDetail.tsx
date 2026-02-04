import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { trackBookingInfoClick, trackContactClick, trackCenterDetailView } from '../utils/analytics';
import type { HealthCenter } from '../types';

interface HealthCenterDetailProps {
  center: HealthCenter | null;
  onClose: () => void;
}

export default function HealthCenterDetail({
  center,
  onClose,
}: HealthCenterDetailProps) {
  const [showAppointmentInfo, setShowAppointmentInfo] = useState(false);

  // Track when center detail is viewed
  useEffect(() => {
    if (center) {
      trackCenterDetailView(center.name);
    }
  }, [center]);

  if (!center) return null;

  // Use original address fields for display
  const displayPhone = center.phone;
  const displayAddress = `${center.street_address_1 || ''}${center.street_address_2 ? `, ${center.street_address_2}` : ''}${center.city_town ? `, ${center.city_town}` : ''}${center.state ? `, ${center.state}` : ''}${center.zipcode ? ` ${center.zipcode}` : ''}`.trim();
  
  // Use OpenAI data for website and types (with final_* fallback)
  const displayWebsite = center.final_website || center.openai_website || center.website;
  const displayTypes = center.all_services || center.final_types || center.openai_types || center.types;
  
  // Appointment information from OpenAI (with final_* fallback)
  const newPatientInstructions = center.final_new_patient_md || center.openai_new_patient_md;
  const otherNotes = center.openai_other_notes_md;
  const sourceUrls = center.openai_source_urls;
  const confidence = center.openai_confidence;

  // Create phone link (tel: protocol works on mobile)
  const phoneLink = displayPhone ? `tel:${displayPhone.replace(/\D/g, '')}` : null;
  
  // Create maps link (Google Maps)
  const mapsLink = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(displayAddress)}`;

  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>
        
        <h1>{center.name}</h1>
        
        <div className="detail-section">
          <h2>Contact Information</h2>
          <p>
            <strong>Address:</strong>{' '}
            <a 
              href={mapsLink} 
              target="_blank" 
              rel="noopener noreferrer"
              className="address-link"
              onClick={() => trackContactClick('maps', center.name)}
            >
              {displayAddress}
            </a>
          </p>
          {displayPhone && (
            <p>
              <strong>Telephone:</strong>{' '}
              <a 
                href={phoneLink || '#'} 
                className="phone-link"
                onClick={() => trackContactClick('phone', center.name)}
              >
                {displayPhone}
              </a>
            </p>
          )}
          {displayWebsite && (
            <p>
              <strong>Website:</strong>{' '}
              <a 
                href={displayWebsite} 
                target="_blank" 
                rel="noopener noreferrer"
                onClick={() => trackContactClick('website', center.name)}
              >
                {displayWebsite}
              </a>
            </p>
          )}
        </div>

        {displayTypes && (
          <div className="detail-section">
            <h2>Services</h2>
            <p>{displayTypes}</p>
          </div>
        )}

        {center.distance !== undefined && (
          <div className="detail-section">
            <h2>Distance</h2>
            <p>{center.distance.toFixed(1)} miles away</p>
          </div>
        )}

        {showAppointmentInfo && (
          <>
            {newPatientInstructions && (
              <div className="detail-section">
                <h2>How to Become a New Patient</h2>
                <div className="markdown-content">
                  <ReactMarkdown>{newPatientInstructions}</ReactMarkdown>
                </div>
              </div>
            )}

            {otherNotes && (
              <div className="detail-section">
                <h2>Other Helpful Notes</h2>
                <div className="markdown-content">
                  <ReactMarkdown>{otherNotes}</ReactMarkdown>
                </div>
              </div>
            )}

            {sourceUrls && (
              <div className="detail-section">
                <h2>Source URLs</h2>
                <div className="source-urls">
                  {sourceUrls.split(',').map((url: string, index: number) => {
                    const trimmedUrl = url.trim();
                    // Check if it's a full URL or just a reference
                    const isUrl = trimmedUrl.startsWith('http://') || trimmedUrl.startsWith('https://');
                    return (
                      <p key={index}>
                        {isUrl ? (
                          <a href={trimmedUrl} target="_blank" rel="noopener noreferrer">
                            {trimmedUrl}
                          </a>
                        ) : (
                          <span>{trimmedUrl}</span>
                        )}
                      </p>
                    );
                  })}
                </div>
              </div>
            )}

            {confidence && (
              <div className="detail-section">
                <h2>Confidence Level of Information</h2>
                <p className="confidence-level">
                  <strong>{confidence}</strong>
                </p>
              </div>
            )}
          </>
        )}

        <div className="detail-section">
          <button 
            className="book-appointment-btn" 
            onClick={() => {
              const newState = !showAppointmentInfo;
              setShowAppointmentInfo(newState);
              // Track when booking info is shown (not hidden)
              if (newState) {
                trackBookingInfoClick(center.name);
              }
            }}
          >
            {showAppointmentInfo ? 'Hide Appointment Information' : 'Booking Info'}
          </button>
        </div>
      </div>
    </div>
  );
}
