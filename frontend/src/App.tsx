import { useState, useEffect } from 'react';
import HealthCenterMap from './components/HealthCenterMap';
import HealthCenterList from './components/HealthCenterList';
import HealthCenterDetail from './components/HealthCenterDetail';
import { loadHealthCenters } from './utils/csvLoader';
import { geocodeZipcode } from './utils/geocoding';
import { calculateDistance } from './utils/distance';
import type { HealthCenter } from './types';
import './App.css';

function App() {
  const [centers, setCenters] = useState<HealthCenter[]>([]);
  const [filteredCenters, setFilteredCenters] = useState<HealthCenter[]>([]);
  const [selectedCenter, setSelectedCenter] = useState<HealthCenter | null>(null);
  const [zipcode, setZipcode] = useState('');
  const [searchZipcode, setSearchZipcode] = useState('');
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [radius, setRadius] = useState(3);

  useEffect(() => {
    loadHealthCenters()
      .then((data) => {
        console.log('Loaded centers:', data.length);
        setCenters(data);
        // Show all centers by default
        setFilteredCenters(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load centers:', err);
        setError('Failed to load health centers data.');
        setLoading(false);
      });
  }, []);

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
      const centersWithDistance = centers
        .filter((center) => center.latitude && center.longitude) // Only centers with valid coordinates
        .map((center) => ({
          ...center,
          distance: calculateDistance(
            location.latitude,
            location.longitude,
            center.latitude,
            center.longitude
          ),
        }))
        .filter((center) => center.distance <= radius)
        .sort((a, b) => (a.distance || 0) - (b.distance || 0));

      console.log(`Found ${centersWithDistance.length} centers within ${radius} miles`);
      setFilteredCenters(centersWithDistance);

      if (centersWithDistance.length === 0) {
        setError(`No centers found within ${radius} miles. Try expanding the radius.`);
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

  return (
    <div className="app">
      <header className="app-header">
        <h1>Community Health Center Search</h1>
        <p className="subtitle">Find nearby community health centers in Massachusetts</p>
      </header>

      <div className="search-section">
        <div className="search-controls">
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
          <button
            onClick={handleSearch}
            disabled={loading || searching || !zipcode.trim()}
            className="search-btn"
          >
            {searching ? 'Searching...' : 'Search'}
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
