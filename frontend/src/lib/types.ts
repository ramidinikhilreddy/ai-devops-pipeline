export type Ticket = {
  key: string;
  title: string;
  summary?: string;
  status: string;
  priority: string;
  assignee: string;
  type: string;
  description?: string;
  labels?: string[];
  created?: string;
  updated?: string;
};

export type PipelineRun = {
  id: string;
  name: string;
  status: string;
  branch: string;
  commit: string;
  startedAt: string;
  duration: string;
  trigger: string;
  ticketKey: string;
  failedTests: number;
  artifacts: string[];
  logs: string[];
  steps: { name: string; status: string; duration: string }[];
  testResults: { name: string; status: string }[];
};

export type PullRequest = {
  id: number;
  title: string;
  repository: string;
  author: string;
  status: string;
  reviewStatus: string;
  branch: string;
  additions: number;
  deletions: number;
  summary: string;
  diffOverview: string[];
};
