import React from 'react';
import CustomDropdown from '../CustomDropdown/CustomDropdown';
import { FACILITY_OWNERS, FACILITY_TYPES } from '../../../../constants/healthcareOptions';

const HealthcareForm = ({ formData, onSelect }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div>
        <label className="block text-lg font-medium mb-3">Facility Owner Type</label>
        <CustomDropdown
          options={FACILITY_OWNERS}
          value={formData.facilityOwnerType}
          onSelect={(value) => onSelect('facilityOwnerType', value)}
          placeholder="Select owner type"
        />
      </div>

      <div>
        <label className="block text-lg font-medium mb-3">Facility Type</label>
        <CustomDropdown
          options={FACILITY_TYPES}
          value={formData.facilityType}
          onSelect={(value) => onSelect('facilityType', value)}
          placeholder="Select facility type"
        />
      </div>
    </div>
  );
};

export default HealthcareForm;