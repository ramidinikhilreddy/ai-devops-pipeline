const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`Request failed for ${path}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getDashboard: () => request('/api/dashboard'),
  getJira: () => request('/api/jira'),
  getGithub: () => request('/api/github'),
  getPipelines: () => request('/api/pipelines'),
  getPullRequests: () => request('/api/pull-requests'),
  getActions: () => request('/api/actions'),
  getReports: () => request('/api/reports'),
  getSettings: () => request('/api/settings'),
  askAssistant: (question: string) =>
    request('/api/assistant/ask', {
      method: 'POST',
      body: JSON.stringify({ question }),
    }),
  createTicket: (payload: { title: string; description: string; priority: string; assignee: string; type: string }) =>
    request('/api/jira/tickets', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  syncTicket: (key: string) => request(`/api/jira/${key}/sync`, { method: 'POST' }),
  triggerPipeline: (key: string) => request(`/api/jira/${key}/trigger-pipeline`, { method: 'POST' }),
  startPipeline: () => request('/api/pipelines/start', { method: 'POST' }),
};
