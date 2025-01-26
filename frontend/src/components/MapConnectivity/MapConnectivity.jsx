import React, { useState } from 'react';
import { APIProvider, Map, Marker } from '@vis.gl/react-google-maps';
import { TailSpin } from 'react-loader-spinner';
import Tabs from './components/Tabs/Tabs';
import LocationInputs from './components/LocationInputs/LocationInputs';
import HealthcareForm from './components/HealthcareForm/HealthcareForm';
import { PAKISTAN_CENTER, MAP_STYLES } from '../../constants/mapSettings';
import { submitData } from '../../utils/api';

const MapConnectivity = () => {
  const [activeTab, setActiveTab] = useState('education');
  const [coordinates, setCoordinates] = useState({ lat: '', lng: '' });
  const [formData, setFormData] = useState({
    healthcare: { facilityOwnerType: '', facilityType: '' }
  });
  const [isLoading, setIsLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleMapClick = (event) => {
    const location = {
      lat: event.detail.latLng.lat,
      lng: event.detail.latLng.lng
    };
    setCoordinates({
      lat: location.lat.toFixed(6),
      lng: location.lng.toFixed(6)
    });
  };

  const handleClear = () => {
    setCoordinates({ lat: '', lng: '' });
    setFormData({ healthcare: { facilityOwnerType: '', facilityType: '' } });
    setApiResponse(null);
    setError(null);
  };

  const isSubmitDisabled = () => {
    if (!coordinates.lat || !coordinates.lng) return true;
    if (activeTab === 'healthcare') {
      return !formData.healthcare.facilityOwnerType || 
             !formData.healthcare.facilityType;
    }
    return false;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setApiResponse(null);

    try {
      if (!coordinates.lat || !coordinates.lng) {
        throw new Error('Please select a location on the map');
      }

      const response = await submitData(activeTab, coordinates, formData[activeTab]);
      setApiResponse(response);
     
    } catch (error) {
      setError(error.message || 'An error occurred');
    } finally {
      setIsLoading(false);
      setCoordinates({ lat: '', lng: '' });
      setFormData({ healthcare: { facilityOwnerType: '', facilityType: '' } });
    }
  };

  return (
    <div className="flex flex-col h-screen relative bg-transparent">
      {isLoading && (
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
          <TailSpin
            height="80"
            width="80"
            color="#4fa94d"
            ariaLabel="tail-spin-loading"
            radius="1"
            visible={true}
          />
        </div>
      )}

      {/* Results Modal */}
      {apiResponse && (
        <div className="absolute inset-0 bg-black/30 flex items-center justify-center z-50 backdrop-blur-sm">
          <div className="bg-white/90 backdrop-blur-lg p-8 rounded-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto border border-gray-200 shadow-2xl">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Analysis Results</h2>
            
            <div className="space-y-4 text-gray-700">
              <div className="flex items-center">
                <span className="font-semibold min-w-[140px]">Demand Score:</span>
                <span className="ml-2 font-mono bg-gray-100 px-2 py-1 rounded">
                  {apiResponse['Demand Score']}
                </span>
              </div>
              

              <div>
                <h3 className="font-semibold mb-2">Recommendations:</h3>
                <div className="whitespace-pre-line bg-gray-50/50 p-4 rounded-lg border border-gray-200">
                  {apiResponse.Recommendations}
                </div>
              </div>
            </div>

            <button
              onClick={() => setApiResponse(null)}
              className="mt-6 px-4 py-2 bg-gray-800/90 hover:bg-gray-700/90 text-white rounded transition-colors backdrop-blur-sm"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Map Section */}
      <div className="flex-[2] relative">
        <APIProvider apiKey={import.meta.env.VITE_GOOGLE_API_KEY}>
          <Map
            style={{ width: '100%', height: '100%' }}
            defaultCenter={PAKISTAN_CENTER}
            defaultZoom={6}
            onClick={handleMapClick}
            options={MAP_STYLES}
          >
            {coordinates.lat && (
              <Marker
                position={{
                  lat: parseFloat(coordinates.lat),
                  lng: parseFloat(coordinates.lng)
                }}
                draggable={true}
                onDragEnd={(event) => {
                  const newLocation = {
                    lat: event.detail.latLng.lat,
                    lng: event.detail.latLng.lng
                  };
                  setCoordinates({
                    lat: newLocation.lat.toFixed(6),
                    lng: newLocation.lng.toFixed(6)
                  });
                }}
                icon={{
                  path: window.google.maps.SymbolPath.CIRCLE,
                  fillColor: '#4285F4',
                  fillOpacity: 1,
                  scale: 8,
                  strokeColor: 'white',
                  strokeWeight: 2
                }}
              />
            )}
          </Map>
        </APIProvider>
      </div>

      {/* Form Section */}
      <div className="flex-[3] bg-transparent border-t border-gray-200/50 shadow-xl">
        <div className="max-w-6xl mx-auto h-full p-8">
          <div className="h-full flex flex-col backdrop-blur-sm bg-white/90 rounded-xl p-6 border border-gray-200/50">
            <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
            
            <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto">
              <div className="space-y-8">
                <LocationInputs lat={coordinates.lat} lng={coordinates.lng} />

                {activeTab === 'healthcare' && (
                  <HealthcareForm
                    formData={formData.healthcare}
                    onSelect={(field, value) => setFormData(prev => ({
                      ...prev,
                      healthcare: { ...prev.healthcare, [field]: value }
                    }))}
                  />
                )}

                <div className="mt-10 flex justify-end space-x-5">
                  <button
                    type="button"
                    onClick={handleClear}
                    className="px-6 py-3 text-lg text-gray-700 border-2 border-gray-300/50 hover:border-gray-400/50 rounded-xl hover:bg-gray-50/50 transition-all"
                  >
                    Clear All
                  </button>
                  <button
                    type="submit"
                    disabled={isSubmitDisabled()}
                    className={`px-6 py-3 rounded-xl text-lg transition-all ${
                      isSubmitDisabled() 
                        ? 'bg-gray-300/50 text-gray-500 cursor-not-allowed'
                        : 'bg-black/90 hover:bg-gray-800/90 text-white backdrop-blur-sm'
                    }`}
                  >
                    Submit
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Error Toast */}
      {error && (
        <div className="fixed bottom-4 right-4 bg-red-100/80 backdrop-blur-sm border border-red-400/50 text-red-700 px-4 py-3 rounded animate-slide-up shadow-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default MapConnectivity;