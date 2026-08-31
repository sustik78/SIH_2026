/**
 * PRAMAN AI - Central API Fetch Utilities with Automatic Bearer Authentication
 */

export const getAuthToken = () => {
  return localStorage.getItem('praman_token') || '';
};

export const getAuthHeaders = (extraHeaders = {}) => {
  const token = getAuthToken();
  const headers = { ...extraHeaders };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const apiFetch = async (url, options = {}) => {
  const headers = getAuthHeaders(options.headers || {});
  return fetch(url, {
    ...options,
    headers
  });
};

export const apiGetJson = async (url, options = {}) => {
  const res = await apiFetch(url, options);
  if (!res.ok) {
    let errorMsg = `Request failed (${res.status})`;
    try {
      const errData = await res.json();
      if (errData && errData.detail) {
        errorMsg = errData.detail;
      }
    } catch (_) {}
    throw new Error(errorMsg);
  }
  return await res.json();
};
