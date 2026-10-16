/**
 * API communication service using standard Fetch API
 */

// Retrieve optional API base URL from Vite environment variable VITE_API_BASE_URL
const rawBase = import.meta.env.VITE_API_BASE_URL?.trim();

// If VITE_API_BASE_URL is provided (e.g. "https://projectlens-api.onrender.com" or "https://api.example.com/api"),
// normalize it so it safely routes to the API endpoints.
// When unset (e.g. local dev), fallback to relative "/api" proxied by Vite.
export const API_BASE = rawBase
  ? (rawBase.replace(/\/+$/, '').endsWith('/api')
      ? rawBase.replace(/\/+$/, '')
      : `${rawBase.replace(/\/+$/, '')}/api`)
  : '/api';

/**
 * Check backend service health and analyzer availability
 */
export async function fetchHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!response.ok) {
      throw new Error(`Health check returned status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.warn('Backend health check error:', error);
    return {
      status: 'offline',
      tools: {
        bandit: { name: 'Bandit', available: false, error: 'Cannot connect to backend service' },
        eslint: { name: 'ESLint', available: false, error: 'Cannot connect to backend service' }
      }
    };
  }
}

/**
 * Fetch educational sample code snippets for quick testing
 */
export async function fetchSampleCodes() {
  try {
    const response = await fetch(`${API_BASE}/samples`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!response.ok) {
      throw new Error(`Failed to load samples: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching samples:', error);
    return [];
  }
}

/**
 * Send source code file to FastAPI backend via multipart/form-data
 * @param {File} file 
 */
export async function analyzeSourceFile(file) {
  if (!file) {
    throw new Error('Please select a file to review.');
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMessage = data?.detail || `Analysis request failed with status ${response.status}`;
      throw new Error(errorMessage);
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      const serverHint = rawBase || 'backend server';
      throw new Error(`Could not connect to the ProjectLens AI backend (${serverHint}). Please verify that the backend is running and CORS is properly configured.`);
    }
    throw error;
  }
}
