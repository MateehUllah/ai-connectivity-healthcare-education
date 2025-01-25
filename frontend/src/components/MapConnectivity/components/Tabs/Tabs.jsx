import React from 'react';

const Tabs = ({ activeTab, setActiveTab }) => {
  return (
    <div className="flex justify-center mb-8">
      <div className="flex items-center bg-gray-200 rounded-full p-1">
        {['education', 'healthcare'].map((tab) => (
          <button
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
            className={`px-8 py-3 rounded-full transition-colors text-lg capitalize ${
              activeTab === tab ? 'bg-black text-white' : 'text-gray-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Tabs;