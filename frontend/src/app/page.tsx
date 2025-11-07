"use client";

import { useState, useEffect } from "react";
import dynamic from 'next/dynamic';
import HealthCenterList from './components/HealthCenterList';

// Dynamically import the map component to avoid SSR issues
const HealthCenterMap = dynamic(() => import('./components/HealthCenterMap'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] bg-gray-100 rounded-lg flex items-center justify-center">
      <p className="text-gray-600">Loading map...</p>
    </div>
  ),
});

interface HealthCenter {
  name: string;
  address: string;
  phone: string;
  types: string;
  website: string;
  zipcode: string;
  street_address_1: string;
  street_address_2?: string;
  city_town: string;
  state: string;
  latitude?: number;
  longitude?: number;
}

export default function Home() {
  const [zipcode, setZipcode] = useState("");
  const [allHealthCenters, setAllHealthCenters] = useState<HealthCenter[]>([]);
  const [filteredHealthCenters, setFilteredHealthCenters] = useState<HealthCenter[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [viewMode, setViewMode] = useState<'list' | 'map' | 'both'>('both');
  const [selectedCenter, setSelectedCenter] = useState<HealthCenter | null>(null);
  const [mapCenter, setMapCenter] = useState<{ lat: number; lng: number } | null>(null);

  // Load all health centers on mount
  useEffect(() => {
    const loadAllCenters = async () => {
      try {
        const response = await fetch('/api/health-centers');
        if (!response.ok) {
          throw new Error("Failed to fetch health centers");
        }
        const data = await response.json();
        setAllHealthCenters(data);
      } catch (err) {
        console.error("Failed to load health centers:", err);
      }
    };
    loadAllCenters();
  }, []);

  const searchByZipcode = async () => {
    if (!zipcode.trim()) {
      setError("Please enter a zipcode");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`/api/health-centers?zipcode=${zipcode}`);
      if (!response.ok) {
        throw new Error("Failed to fetch health centers");
      }
      const data = await response.json();
      setFilteredHealthCenters(data);
      
      // Zoom map to the first result's location
      if (data.length > 0 && data[0].latitude && data[0].longitude) {
        const newCenter = { lat: data[0].latitude, lng: data[0].longitude };
        console.log('Setting map center to:', newCenter);
        setMapCenter(newCenter);
      } else {
        console.log('No valid coordinates in search results');
      }
    } catch (err) {
      setError("Failed to load health centers. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    searchByZipcode();
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Community Health Centers
          </h1>
          <p className="text-lg text-gray-600">
            Find health centers by zipcode
          </p>
        </header>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8 max-w-md mx-auto">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="zipcode" className="block text-sm font-medium text-gray-700 mb-2">
                Enter Zipcode
              </label>
              <input
                type="text"
                id="zipcode"
                value={zipcode}
                onChange={(e) => setZipcode(e.target.value)}
                placeholder="e.g., 02138, 02139"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 placeholder-gray-400"
                maxLength={5}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200 font-medium disabled:opacity-50"
            >
              {loading ? "Searching..." : "Search Health Centers"}
            </button>
          </form>
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Map View - Always Visible */}
        {allHealthCenters.length > 0 && (
          <div className="space-y-6">
            {/* View Mode Toggle */}
            <div className="bg-white rounded-lg shadow-lg p-4">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-semibold text-gray-800">
                  {zipcode
                    ? filteredHealthCenters.length > 0
                      ? `Health Centers in ${zipcode} (${filteredHealthCenters.length} found)`
                      : `No Health Centers in ${zipcode}`
                    : `All Health Centers (${allHealthCenters.length} total)`}
                </h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => setViewMode('list')}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      viewMode === 'list'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    📋 List
                  </button>
                  <button
                    onClick={() => setViewMode('map')}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      viewMode === 'map'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    🗺️ Map
                  </button>
                  <button
                    onClick={() => setViewMode('both')}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      viewMode === 'both'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    📍 Both
                  </button>
                </div>
              </div>
            </div>

            {/* Map View */}
            {(viewMode === 'map' || viewMode === 'both') && allHealthCenters.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  {zipcode ? `Map - Showing ${zipcode} area` : 'Map - All Health Centers'}
                </h3>
                <HealthCenterMap 
                  healthCenters={allHealthCenters} 
                  highlightedCenters={filteredHealthCenters}
                  center={mapCenter}
                  zoom={mapCenter ? 13 : 8}
                />
              </div>
            )}

            {/* List View */}
            {(viewMode === 'list' || viewMode === 'both') && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">List View</h3>
                <HealthCenterList 
                  healthCenters={zipcode && filteredHealthCenters.length > 0 ? filteredHealthCenters : allHealthCenters}
                  onCenterClick={(center) => setSelectedCenter(center)}
                />
              </div>
            )}
          </div>
        )}

        {/* No Results */}
        {filteredHealthCenters.length === 0 && !loading && zipcode && allHealthCenters.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-gray-500">
              <div className="mb-4">
                <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.709M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <p className="text-lg">No health centers found in zipcode {zipcode}</p>
              <p className="text-sm mt-2">Try a different zipcode or explore the map to see nearby centers</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
