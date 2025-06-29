import axios from 'axios';
import type { QueryRequest, QueryResponse, ReportRequest, ReportResponse, Jurisdiction } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchCaseLaw = async (request: QueryRequest): Promise<QueryResponse> => {
  try {
    const response = await apiClient.post<QueryResponse>('/search', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to search case law');
    }
    throw new Error('An unexpected error occurred');
  }
};

export const generateReport = async (request: ReportRequest): Promise<ReportResponse> => {
  try {
    const response = await apiClient.post<ReportResponse>('/generate-report', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to generate report');
    }
    throw new Error('An unexpected error occurred');
  }
};

export const getJurisdictions = async (): Promise<Jurisdiction[]> => {
  try {
    const response = await apiClient.get('/jurisdictions');
    return response.data.jurisdictions;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch jurisdictions');
    }
    throw new Error('An unexpected error occurred');
  }
};

export const healthCheck = async (): Promise<{ status: string; timestamp: string }> => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch {
    throw new Error('Backend service unavailable');
  }
};
