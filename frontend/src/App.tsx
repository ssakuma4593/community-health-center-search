import { useState, useEffect } from 'react';
import HealthCenterMap from './components/HealthCenterMap';
import HealthCenterList from './components/HealthCenterList';
import HealthCenterDetail from './components/HealthCenterDetail';
import { loadHealthCenters } from './utils/csvLoader';
import { geocodeZipcode } from './utils/geocoding';
import { calculateDistance } from './utils/distance';
import { trackZipcodeSearch, trackServiceFilterToggle } from './utils/analytics';
import type { HealthCenter } from './types';
import './App.css';

function App() {
  console.log('App component rendering...');
  
  const [centers, setCenters] = useState<HealthCenter[]>([]);
  const [filteredCenters, setFilteredCenters] = useState<HealthCenter[]>([]);
  const [selectedCenter, setSelectedCenter] = useState<HealthCenter | null>(null);
  const [zipcode, setZipcode] = useState('');
  const [searchZipcode, setSearchZipcode] = useState('');
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [radius, setRadius] = useState(3);
  // Service type filters
  const [filterPrimaryCare, setFilterPrimaryCare] = useState(false);
  const [filterDentalCare, setFilterDentalCare] = useState(false);
  const [filterVision, setFilterVision] = useState(false);
  const [filterBehavioralHealth, setFilterBehavioralHealth] = useState(false);
  const [filterPharmacy, setFilterPharmacy] = useState(false);

  useEffect(() => {
    console.log('useEffect running - about to call loadHealthCenters()');
    console.log('App mounted, loading health centers...');
    loadHealthCenters()
      .then((data) => {
        console.log('Loaded centers:', data.length);
        if (data && data.length > 0) {
          setCenters(data);
          // Show all centers by default
          setFilteredCenters(data);
        } else {
          console.warn('No centers loaded - empty array returned');
          setError('No health centers data available. Please check the console for details.');
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load centers:', err);
        setError(`Failed to load health centers data: ${err instanceof Error ? err.message : 'Unknown error'}. Please check the console and network tab.`);
        setLoading(false);
      });
  }, []);

  // Re-apply service type filters when filters change (only when no zipcode search is active)
  useEffect(() => {
    if (centers.length === 0 || loading) return; // Don't filter until centers are loaded
    if (searchZipcode) return; // Skip if zipcode search is active (handled in handleSearch)
    
    // Apply service type filters to all centers
    const hasAnyFilter = filterPrimaryCare || filterDentalCare || filterVision || filterBehavioralHealth;
    if (!hasAnyFilter) {
      setFilteredCenters(centers);
      return;
    }

    const filtered = centers.filter((center) => {
      const matches = [];
      if (filterPrimaryCare && center.has_primary_care) matches.push(true);
      if (filterDentalCare && center.has_dental_care) matches.push(true);
      if (filterVision && center.has_vision) matches.push(true);
      if (filterBehavioralHealth && center.has_behavioral_health) matches.push(true);
      return matches.length > 0;
    });

    setFilteredCenters(filtered);
  }, [centers, filterPrimaryCare, filterDentalCare, filterVision, filterBehavioralHealth, filterPharmacy, searchZipcode, loading]);

  const handleSearch = async () => {
    if (!zipcode.trim()) {
      setError('Please enter a zipcode');
      return;
    }

    setSearching(true);
    setError(null);
    setSelectedCenter(null);

    try {
      console.log('Searching for zipcode:', zipcode);
      console.log('Total centers loaded:', centers.length);
      
      const location = await geocodeZipcode(zipcode);
      console.log('Geocoded location:', location);
      
      if (!location) {
        setError('Could not find location for that zipcode. Please try another.');
        setSearching(false);
        return;
      }

      setSearchZipcode(zipcode);

      // Calculate distances and filter
      const validCenters = centers.filter((center) => center.latitude && center.longitude);
      console.log(`Total centers: ${centers.length}, Valid coordinates: ${validCenters.length}`);
      
      const centersWithDistance = validCenters
        .map((center) => {
          const distance = calculateDistance(
            location.latitude,
            location.longitude,
            center.latitude,
            center.longitude
          );
          return {
            ...center,
            distance,
          };
        })
        .filter((center) => {
          const withinRadius = center.distance <= radius;
          if (!withinRadius && center.distance <= radius + 1) {
            console.log(`Center "${center.name}" is ${center.distance.toFixed(2)} miles away (just outside ${radius} mile radius)`);
          }
          return withinRadius;
        })
        .sort((a, b) => (a.distance || 0) - (b.distance || 0));

      // Apply service type filters to distance-filtered results
      const hasAnyFilter = filterPrimaryCare || filterDentalCare || filterVision || filterBehavioralHealth || filterPharmacy;
      let finalFiltered = centersWithDistance;
      if (hasAnyFilter) {
        finalFiltered = centersWithDistance.filter((center) => {
          // If center has no service type data, always include it
          const hasNoServiceData = !center.all_services && !center.final_types && !center.openai_types && !center.types;
          if (hasNoServiceData) {
            return true;
          }
          
          // Otherwise, check if it matches any selected filter
          const matches = [];
          if (filterPrimaryCare && center.has_primary_care) matches.push(true);
          if (filterDentalCare && center.has_dental_care) matches.push(true);
          if (filterVision && center.has_vision) matches.push(true);
          if (filterBehavioralHealth && center.has_behavioral_health) matches.push(true);
          if (filterPharmacy && center.has_pharmacy) matches.push(true);
          return matches.length > 0;
        });
      }

      console.log(`Found ${finalFiltered.length} centers within ${radius} miles (after service filters)`);
      console.log(`Search location: ${location.latitude}, ${location.longitude}`);
      if (finalFiltered.length > 0) {
        console.log('Closest centers:', finalFiltered.slice(0, 3).map(c => `${c.name}: ${c.distance.toFixed(2)} miles`));
      }
      setFilteredCenters(finalFiltered);

      // Track zipcode search event
      const activeFilters: string[] = [];
      if (filterPrimaryCare) activeFilters.push('primary_care');
      if (filterDentalCare) activeFilters.push('dental_care');
      if (filterVision) activeFilters.push('vision');
      if (filterBehavioralHealth) activeFilters.push('behavioral_health');
      
      trackZipcodeSearch(zipcode, radius, finalFiltered.length, activeFilters);

      // Track zipcode search event
      trackZipcodeSearch(zipcode, radius, centersWithDistance.length, []);

      if (centersWithDistance.length === 0) {
        setError(`No centers found within ${radius} miles. Try expanding the radius.`);
      if (finalFiltered.length === 0) {
        setError(`No centers found within ${radius} miles matching the selected filters. Try expanding the radius or adjusting filters.`);
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('An error occurred during search. Please try again.');
    } finally {
      setSearching(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // Debug: Log current state
  if (process.env.NODE_ENV === 'development') {
    console.log('App render - loading:', loading, 'centers:', centers.length, 'filtered:', filteredCenters.length);
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Community Health Center Search</h1>
        <p className="subtitle">Find nearby community health centers in Massachusetts</p>
      </header>

      <div className="search-section">
        <div className="search-controls-row">
          <div className="search-input-group">
            <label htmlFor="zipcode">Enter Zipcode:</label>
            <input
              id="zipcode"
              type="text"
              value={zipcode}
              onChange={(e) => setZipcode(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="e.g., 02138"
              maxLength={5}
              disabled={loading || searching}
            />
          </div>
          <div className="radius-control">
            <label htmlFor="radius">Radius (miles):</label>
            <select
              id="radius"
              value={radius}
              onChange={(e) => setRadius(Number(e.target.value))}
              disabled={loading || searching}
            >
              <option value={3}>3</option>
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={50}>50</option>
            </select>
          </div>
        </div>

        <div className="search-controls-row">
          <div className="filter-checkboxes">
            <label className="filter-checkbox">
              <input
                type="checkbox"
                checked={filterPrimaryCare}
                onChange={(e) => {
                  const enabled = e.target.checked;
                  setFilterPrimaryCare(enabled);
                  trackServiceFilterToggle('primary_care', enabled);
                }}
                disabled={loading}
              />
              <span>Primary Care</span>
            </label>
            <label className="filter-checkbox">
              <input
                type="checkbox"
                checked={filterDentalCare}
                onChange={(e) => {
                  const enabled = e.target.checked;
                  setFilterDentalCare(enabled);
                  trackServiceFilterToggle('dental_care', enabled);
                }}
                disabled={loading}
              />
              <span>Dental Care</span>
            </label>
            <label className="filter-checkbox">
              <input
                type="checkbox"
                checked={filterVision}
                onChange={(e) => {
                  const enabled = e.target.checked;
                  setFilterVision(enabled);
                  trackServiceFilterToggle('vision', enabled);
                }}
                disabled={loading}
              />
              <span>Vision</span>
            </label>
            <label className="filter-checkbox">
              <input
                type="checkbox"
                checked={filterBehavioralHealth}
                onChange={(e) => {
                  const enabled = e.target.checked;
                  setFilterBehavioralHealth(enabled);
                  trackServiceFilterToggle('behavioral_health', enabled);
                }}
                disabled={loading}
              />
              <span>Behavioral Health</span>
            </label>
            <label className="filter-checkbox">
              <input
                type="checkbox"
                checked={filterPharmacy}
                onChange={(e) => {
                  const enabled = e.target.checked;
                  setFilterPharmacy(enabled);
                  trackServiceFilterToggle('pharmacy', enabled);
                }}
                disabled={loading}
              />
              <span>Pharmacy</span>
            </label>
          </div>
          <button
            onClick={handleSearch}
            disabled={loading || searching || !zipcode.trim()}
            className="search-btn"
          >
            {searching ? 'Searching' : 'Search'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}
        {searchZipcode && !error && (
          <div className="search-info">
            Showing results for zipcode: <strong>{searchZipcode}</strong>
          </div>
        )}
      </div>

      {loading && (
        <div className="loading">
          <p>Loading health centers data...</p>
        </div>
      )}

      {!loading && filteredCenters.length > 0 && (
        <div className="results-section">
          <div className="map-wrapper">
            <HealthCenterMap
              centers={filteredCenters}
              selectedCenter={selectedCenter}
              onCenterClick={setSelectedCenter}
            />
          </div>
          <HealthCenterList
            centers={filteredCenters}
            selectedCenter={selectedCenter}
            onCenterClick={setSelectedCenter}
            isFiltered={!!searchZipcode}
          />
        </div>
      )}

      {!loading && filteredCenters.length === 0 && searchZipcode && (
        <div className="results-section">
          <div className="no-results">
            <p>No centers found within {radius} miles of {searchZipcode}.</p>
            <p>Try expanding the radius or searching a different zipcode.</p>
          </div>
        </div>
      )}

      {selectedCenter && (
        <HealthCenterDetail
          center={selectedCenter}
          onClose={() => setSelectedCenter(null)}
        />
      )}
    </div>
  );
}

export default App;
