import axios from 'axios';
import { ApiResponse, FilterOptions, ChartFilters } from '../types/api';

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://ausvisa-backend.built.au/api'
  : 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const apiService = {
  async getFilterOptions(): Promise<FilterOptions> {
    const response = await api.get<FilterOptions>('/data/filter-options/');
    return response.data;
  },

  async getVisaData(filters: ChartFilters = {}): Promise<ApiResponse> {
    const params = new URLSearchParams();

    // Handle multiple visa types
    if (filters.visa_types && filters.visa_types.length > 0) {
      filters.visa_types.forEach(type => params.append('visa_type', type));
    }

    // Handle multiple occupations
    if (filters.occupations && filters.occupations.length > 0) {
      filters.occupations.forEach(occupation => params.append('occupation', occupation));
    }

    // Handle multiple points
    if (filters.points && filters.points.length > 0) {
      filters.points.forEach(points => params.append('points', points.toString()));
    }

    // Handle multiple EOI statuses
    if (filters.eoi_statuses && filters.eoi_statuses.length > 0) {
      filters.eoi_statuses.forEach(status => params.append('eoi_status', status));
    }

    const response = await api.get<ApiResponse>(`/data/visa-data/?${params.toString()}`);
    return response.data;
  }
};