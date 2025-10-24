"use client";

import { useState, useEffect } from "react";

interface HealthCenter {
  name: string;
  address: string;
  phone: string;
  types: string;
  website: string;
  zipcode: string;
}

export default function MapPage() {
  const [zipcode, setZipcode] = useState("");
  const [healthCenters, setHealthCenters] = useState<HealthCenter[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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
      setHealthCenters(data);
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
            Community Health Centers Map
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
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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

        {/* Results */}
        {healthCenters.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Health Centers in {zipcode} ({healthCenters.length} found)
            </h2>
            <div className="grid gap-4">
              {healthCenters.map((center, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {center.name}
                  </h3>
                  <div className="space-y-1 text-sm text-gray-600">
                    <p><strong>Address:</strong> {center.address}</p>
                    <p><strong>Phone:</strong> {center.phone}</p>
                    <p><strong>Services:</strong> {center.types}</p>
                    {center.website && (
                      <p>
                        <strong>Website:</strong>{" "}
                        <a 
                          href={center.website} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 underline"
                        >
                          {center.website}
                        </a>
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {healthCenters.length === 0 && !loading && zipcode && (
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-gray-500">
              <div className="mb-4">
                <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.709M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <p className="text-lg">No health centers found in zipcode {zipcode}</p>
              <p className="text-sm mt-2">Try a different zipcode or check nearby areas</p>
            </div>
          </div>
        )}

        {/* Instructions */}
        {!zipcode && (
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-gray-500">
              <div className="mb-4">
                <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <p className="text-lg">Enter a zipcode to find nearby health centers</p>
              <p className="text-sm mt-2">Search for community health centers in your area</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
