import React from 'react';

const LocationInputs = ({ lat, lng }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label className="block text-lg font-medium mb-2">Latitude</label>
        <input
          type="text"
          value={lat}
          disabled
          className="w-full p-3 border-2 rounded-xl bg-gray-100 text-lg"
        />
      </div>
      <div>
        <label className="block text-lg font-medium mb-2">Longitude</label>
        <input
          type="text"
          value={lng}
          disabled
          className="w-full p-3 border-2 rounded-xl bg-gray-100 text-lg"
        />
      </div>
    </div>
  );
};

export default LocationInputs;