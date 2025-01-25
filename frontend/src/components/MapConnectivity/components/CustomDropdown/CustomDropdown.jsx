import React, { useState } from 'react';
import useClickOutside from '../../../../hooks/useClickOutside';

const CustomDropdown = ({ options, value, onSelect, placeholder }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useClickOutside(() => setIsOpen(false));

  const filteredOptions = options.filter(option =>
    option.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="relative" ref={dropdownRef}>
      <div className="relative">
        <input
          type="text"
          readOnly
          value={value}
          onClick={() => setIsOpen(!isOpen)}
          className="w-full p-4 border-2 rounded-xl bg-white focus:ring-4 focus:ring-blue-300 cursor-pointer text-lg"
          placeholder={placeholder}
        />
        <div className="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
          <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      {isOpen && (
        <div className="absolute z-10 w-full mt-2 bg-white border-2 rounded-xl shadow-2xl max-h-80 overflow-y-auto">
          <div className="p-3 border-b-2">
            <input
              type="text"
              placeholder="Search..."
              className="w-full p-3 text-lg border-2 rounded-lg"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="divide-y">
            {filteredOptions.map(option => (
              <div
                key={option}
                onClick={() => {
                  onSelect(option);
                  setIsOpen(false);
                  setSearchQuery('');
                }}
                className="p-4 cursor-pointer hover:bg-blue-50 transition-colors text-lg"
              >
                {option}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomDropdown;