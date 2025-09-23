export interface VisaDataRecord {
  id: number;
  month_year: string;
  visa_type: string;
  occupation: string;
  eoi_status: string;
  points: number;
  count_eois: number;
}

export interface FilterOptions {
  visa_types: string[];
  occupations: string[];
  month_years: string[];
  eoi_statuses: string[];
  points: number[];
}

export interface ApiResponse {
  count: number;
  results: VisaDataRecord[];
}

export interface ChartFilters {
  visa_types?: string[];
  occupations?: string[];
  points?: number[];
  eoi_statuses?: string[];
}

export interface SelectOption {
  value: string | number;
  label: string;
}