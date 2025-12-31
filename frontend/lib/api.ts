import { supabase } from './supabase'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function getAuthToken() {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token
}

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const token = await getAuthToken()
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }))
    throw new Error(error.message || 'Request failed')
  }

  return response.json()
}

// Specific API functions
export const api = {
  // User Profile
  createProfile: (data: {
    user_id: string
    full_name: string
    career_goal: string
    experience_level: string
  }) => apiRequest('/api/users/profile', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  getProfile: () => apiRequest('/api/users/profile'),

  // Jobs
  getJobs: () => apiRequest('/api/jobs'),
  
  matchJobs: () => apiRequest('/api/jobs/match'),

  // Agents
  analyzeProfile: (data: any) => apiRequest('/api/profile/analyze', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
}