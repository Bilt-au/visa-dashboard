import React from 'react';
import Select, { MultiValue } from 'react-select';
import { FilterOptions, ChartFilters, SelectOption } from '../types/api';

interface FilterPanelProps {
  filterOptions: FilterOptions | null;
  filters: ChartFilters;
  onFiltersChange: (filters: ChartFilters) => void;
  onApply: () => void;
  loading: boolean;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filterOptions,
  filters,
  onFiltersChange,
  onApply,
  loading
}) => {
  const handleVisaTypesChange = (selectedOptions: MultiValue<SelectOption>) => {
    onFiltersChange({
      ...filters,
      visa_types: selectedOptions.map(option => option.value as string)
    });
  };

  const handleOccupationsChange = (selectedOptions: MultiValue<SelectOption>) => {
    onFiltersChange({
      ...filters,
      occupations: selectedOptions.map(option => option.value as string)
    });
  };

  const handlePointsChange = (selectedOptions: MultiValue<SelectOption>) => {
    onFiltersChange({
      ...filters,
      points: selectedOptions.map(option => option.value as number)
    });
  };

  const handleStatusChange = (selectedOptions: MultiValue<SelectOption>) => {
    onFiltersChange({
      ...filters,
      eoi_statuses: selectedOptions.map(option => option.value as string)
    });
  };

  if (!filterOptions) {
    return <div className="filter-panel loading">Loading filters...</div>;
  }

  // Convert options to react-select format
  const visaTypeOptions: SelectOption[] = filterOptions.visa_types.map(type => ({
    value: type,
    label: type
  }));

  const occupationOptions: SelectOption[] = filterOptions.occupations.map(occupation => ({
    value: occupation,
    label: occupation
  }));

  const pointsOptions: SelectOption[] = filterOptions.points.map(points => ({
    value: points,
    label: points.toString()
  }));

  const statusOptions: SelectOption[] = filterOptions.eoi_statuses.map(status => ({
    value: status,
    label: status
  }));

  // Convert current selections to react-select format
  const selectedVisaTypes = visaTypeOptions.filter(option =>
    filters.visa_types?.includes(option.value as string)
  );

  const selectedOccupations = occupationOptions.filter(option =>
    filters.occupations?.includes(option.value as string)
  );

  const selectedPoints = pointsOptions.filter(option =>
    filters.points?.includes(option.value as number)
  );

  const selectedStatuses = statusOptions.filter(option =>
    filters.eoi_statuses?.includes(option.value as string)
  );

  const customSelectStyles = {
    control: (provided: any) => ({
      ...provided,
      border: '2px solid #e1e8ed',
      borderRadius: '8px',
      padding: '4px',
      boxShadow: 'none',
      '&:hover': {
        borderColor: '#667eea'
      }
    }),
    multiValue: (provided: any) => ({
      ...provided,
      backgroundColor: '#667eea',
      borderRadius: '4px'
    }),
    multiValueLabel: (provided: any) => ({
      ...provided,
      color: 'white',
      fontSize: '14px'
    }),
    multiValueRemove: (provided: any) => ({
      ...provided,
      color: 'white',
      ':hover': {
        backgroundColor: '#764ba2',
        color: 'white'
      }
    })
  };

  return (
    <div className="filter-panel">
      <h3>🔍 Multi-Select Filters</h3>

      <div className="filter-row">
        <div className="filter-group">
          <label>Visa Types:</label>
          <Select
            isMulti
            options={visaTypeOptions}
            value={selectedVisaTypes}
            onChange={handleVisaTypesChange}
            placeholder="Search and select visa types..."
            isSearchable={true}
            styles={customSelectStyles}
            closeMenuOnSelect={false}
            hideSelectedOptions={false}
            className="react-select-container"
            classNamePrefix="react-select"
          />
        </div>

        <div className="filter-group">
          <label>Occupations:</label>
          <Select
            isMulti
            options={occupationOptions}
            value={selectedOccupations}
            onChange={handleOccupationsChange}
            placeholder="Search and select occupations..."
            isSearchable={true}
            styles={customSelectStyles}
            closeMenuOnSelect={false}
            hideSelectedOptions={false}
            className="react-select-container"
            classNamePrefix="react-select"
          />
        </div>

        <div className="filter-group">
          <label>Points:</label>
          <Select
            isMulti
            options={pointsOptions}
            value={selectedPoints}
            onChange={handlePointsChange}
            placeholder="Search and select points..."
            isSearchable={true}
            styles={customSelectStyles}
            closeMenuOnSelect={false}
            hideSelectedOptions={false}
            className="react-select-container"
            classNamePrefix="react-select"
          />
        </div>

        <div className="filter-group">
          <label>EOI Status:</label>
          <Select
            isMulti
            options={statusOptions}
            value={selectedStatuses}
            onChange={handleStatusChange}
            placeholder="Search and select EOI statuses..."
            isSearchable={true}
            styles={customSelectStyles}
            closeMenuOnSelect={false}
            hideSelectedOptions={false}
            className="react-select-container"
            classNamePrefix="react-select"
          />
        </div>
      </div>

      <div className="filter-actions">
        <button
          className="apply-button"
          onClick={onApply}
          disabled={loading}
        >
          {loading ? 'Loading...' : '🚀 Apply Filters & Show Chart'}
        </button>

        <button
          className="clear-button"
          onClick={() => onFiltersChange({})}
          disabled={loading}
        >
          Clear All
        </button>
      </div>
    </div>
  );
};

export default FilterPanel;