import { useEffect, useMemo, useState } from 'react';
import {
  Bot,
  FolderGit2,
  Gauge,
  Github,
  GitPullRequest,
  PlayCircle,
  Settings,
  Workflow,
  BarChart3,
  Ticket,
  RefreshCw,
  PlusCircle,
  Search,
} from 'lucide-react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { api } from './lib/api';
import type { PipelineRun, PullRequest, Ticket as TicketType } from './lib/types';
import { Badge, SectionCard, StatCard } from './components/ui';

type DashboardResponse = {
  metrics: {
    totalTickets: number;
    activePipelineRuns: number;
    failedTests: number;
    openPrs: number;
    recentAgentActivity: number;
  };
  tickets: TicketType[];
  pipelineRuns: PipelineRun[];
  pullRequests: PullRequest[];
  agentActivity: { agent: string; action: string; time: string; status: string }[];
};

type GithubResponse = {
  repositories: { name: string; private: boolean; defaultBranch: string; stars: number; openPrs: number }[];
  branches: { name: string; lastCommit: string; status: string }[];
  commits: { sha: string; message: string; author: string; time: string }[];
  pullRequests: PullRequest[];
  workflowRuns: { name: string; status: string; failedJobs: number; retryUrl: string }[];
};

type ReportsResponse = {
  passFailTrends: { label: string; passed: number; failed: number }[];
  agentSuccessRate: { name: string; value: number }[];
  jiraCycleTime: { name: string; days: number }[];
  prThroughput: { label: string; value: number }[];
};

type SettingsResponse = {
  jira: Record<string, string | boolean | number>;
  github: Record<string, string | boolean | number>;
  llm: Record<string, string | boolean | number>;
  vectorDb: Record<string, string | boolean | number>;
};

type PageKey = 'dashboard' | 'jira' | 'github' | 'pipelines' | 'pulls' | 'actions' | 'assistant' | 'reports' | 'settings';

const NAV = [
  { key: 'dashboard', label: 'Dashboard', icon: Gauge },
  { key: 'jira', label: 'Jira Workspace', icon: Ticket },
  { key: 'github', label: 'GitHub Workspace', icon: Github },
  { key: 'pipelines', label: 'Pipeline Runs', icon: PlayCircle },
  { key: 'pulls', label: 'Pull Requests', icon: GitPullRequest },
  { key: 'actions', label: 'GitHub Actions', icon: Workflow },
  { key: 'assistant', label: 'AI Assistant', icon: Bot },
  { key: 'reports', label: 'Reports', icon: BarChart3 },
  { key: 'settings', label: 'Settings', icon: Settings },
] as const;

function App() {
  const [page, setPage] = useState<PageKey>('dashboard');
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [github, setGithub] = useState<GithubResponse | null>(null);
  const [reports, setReports] = useState<ReportsResponse | null>(null);
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [assistantQuestion, setAssistantQuestion] = useState('What should I fix next in the project?');
  const [assistantAnswer, setAssistantAnswer] = useState('');
  const [ticketForm, setTicketForm] = useState({
    title: 'Generated ticket from workspace',
    description: 'Create a new delivery task and trigger the pipeline.',
    priority: 'Medium',
    assignee: 'Mahdi',
    type: 'Task',
  });

  async function loadData() {
    setLoading(true);
    try {
      const [dashboardData, githubData, reportsData, settingsData] = await Promise.all([
        api.getDashboard(),
        api.getGithub(),
        api.getReports(),
        api.getSettings(),
      ]);
      setDashboard(dashboardData as DashboardResponse);
      setGithub(githubData as GithubResponse);
      setReports(reportsData as ReportsResponse);
      setSettings(settingsData as SettingsResponse);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function askAssistant() {
    const result = (await api.askAssistant(assistantQuestion)) as { answer: string };
    setAssistantAnswer(result.answer);
  }

  async function createTicket() {
    await api.createTicket(ticketForm);
    await loadData();
    setPage('jira');
  }

  const content = useMemo(() => {
    if (loading || !dashboard || !github || !reports || !settings) {
      return <div className="panel"><p>Loading project workspace...</p></div>;
    }

    const tickets = dashboard.tickets;
    const runs = dashboard.pipelineRuns;
    const prs = dashboard.pullRequests;
    const activity = dashboard.agentActivity;

    if (page === 'dashboard') {
      const statusCounts = ['To Do', 'In Progress', 'In Review', 'Done'].map((status) => ({
        name: status,
        value: tickets.filter((ticket) => ticket.status === status).length,
      }));

      return (
        <>
          <div className="hero panel">
            <div>
              <div className="eyebrow">AI + DevOps Dashboard</div>
              <h1>AI DevOps Platform</h1>
              <p className="muted">
                Jira, GitHub, pipeline telemetry, and agent insights in one working interface.
              </p>
            </div>
            <div className="hero-actions">
              <button className="primary" onClick={() => setPage('jira')}>Open Jira Workspace</button>
              <button className="secondary" onClick={() => setPage('assistant')}>Ask AI Assistant</button>
            </div>
          </div>

          <div className="stats-grid">
            <StatCard title="Total tickets" value={dashboard.metrics.totalTickets} hint="Across current Jira board" />
            <StatCard title="Active pipeline runs" value={dashboard.metrics.activePipelineRuns} hint="Currently executing" />
            <StatCard title="Failed tests" value={dashboard.metrics.failedTests} hint="Across recent runs" />
            <StatCard title="Open PRs" value={dashboard.metrics.openPrs} hint="Waiting for review" />
            <StatCard title="Recent agent activity" value={dashboard.metrics.recentAgentActivity} hint="Last hour" />
          </div>

          <div className="two-col">
            <SectionCard title="Ticket status" subtitle="Board distribution from Jira workspace">
              <div className="chart-box">
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={statusCounts}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar dataKey="value" radius={[10, 10, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </SectionCard>
            <SectionCard title="Recent pipeline health" subtitle="Pass and fail count for latest trend window">
              <div className="chart-box">
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={reports.passFailTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="label" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="passed" strokeWidth={2} />
                    <Line type="monotone" dataKey="failed" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </SectionCard>
          </div>

          <div className="two-col">
            <SectionCard title="Open pull requests" subtitle="Generated PRs, summaries, and review states">
              <DataTable
                columns={['PR', 'Branch', 'Status', 'Review']}
                rows={prs.map((pr) => [
                  `#${pr.id} ${pr.title}`,
                  pr.branch,
                  pr.status,
                  pr.reviewStatus,
                ])}
              />
            </SectionCard>
            <SectionCard title="Recent agent activity" subtitle="Planner, review, and RAG actions">
              <div className="stack-list">
                {activity.map((item) => (
                  <div className="list-item" key={`${item.agent}-${item.time}`}>
                    <div>
                      <strong>{item.agent}</strong>
                      <div className="muted small">{item.action}</div>
                    </div>
                    <div className="right-meta">
                      <Badge tone={item.status === 'running' ? 'warning' : 'success'}>{item.status}</Badge>
                      <span className="muted small">{item.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </SectionCard>
          </div>
        </>
      );
    }

    if (page === 'jira') {
      const selected = tickets[0];
      return (
        <div className="two-col layout-wide">
          <SectionCard
            title="Jira Workspace"
            subtitle="Ticket list, create flow, sync, and pipeline trigger"
            action={
              <div className="inline-actions">
                <button className="secondary" onClick={async () => { await api.syncTicket(selected.key); await loadData(); }}><RefreshCw size={16} /> Sync</button>
                <button className="primary" onClick={async () => { await api.triggerPipeline(selected.key); await loadData(); }}>Trigger pipeline</button>
              </div>
            }
          >
            <div className="search-row"><Search size={16} /><input value={selected.title} readOnly /></div>
            <DataTable
              columns={['Key', 'Title', 'Status', 'Priority', 'Assignee']}
              rows={tickets.map((ticket) => [ticket.key, ticket.title, ticket.status, ticket.priority, ticket.assignee])}
            />
          </SectionCard>
          <div className="column-stack">
            <SectionCard title="Ticket detail" subtitle={selected.key}>
              <div className="detail-grid">
                <InfoRow label="Summary" value={selected.summary || selected.title} />
                <InfoRow label="Type" value={selected.type} />
                <InfoRow label="Priority" value={selected.priority} />
                <InfoRow label="Assignee" value={selected.assignee} />
                <InfoRow label="Description" value={selected.description || '-'} />
              </div>
            </SectionCard>
            <SectionCard title="Create / update ticket" subtitle="Prototype form backed by FastAPI mock API">
              <div className="form-grid">
                <input value={ticketForm.title} onChange={(e) => setTicketForm({ ...ticketForm, title: e.target.value })} placeholder="Title" />
                <input value={ticketForm.assignee} onChange={(e) => setTicketForm({ ...ticketForm, assignee: e.target.value })} placeholder="Assignee" />
                <select value={ticketForm.priority} onChange={(e) => setTicketForm({ ...ticketForm, priority: e.target.value })}>
                  <option>Low</option><option>Medium</option><option>High</option><option>Highest</option>
                </select>
                <select value={ticketForm.type} onChange={(e) => setTicketForm({ ...ticketForm, type: e.target.value })}>
                  <option>Task</option><option>Story</option><option>Bug</option><option>Epic</option>
                </select>
                <textarea value={ticketForm.description} onChange={(e) => setTicketForm({ ...ticketForm, description: e.target.value })} rows={4} />
                <button className="primary" onClick={createTicket}><PlusCircle size={16} /> Create ticket</button>
              </div>
            </SectionCard>
          </div>
        </div>
      );
    }

    if (page === 'github') {
      return (
        <div className="two-col layout-wide">
          <SectionCard title="Repositories" subtitle="GitHub workspace overview">
            <DataTable
              columns={['Repository', 'Default branch', 'Open PRs', 'Visibility']}
              rows={github.repositories.map((repo) => [repo.name, repo.defaultBranch, String(repo.openPrs), repo.private ? 'Private' : 'Public'])}
            />
          </SectionCard>
          <div className="column-stack">
            <SectionCard title="Branches" subtitle="Active delivery branches">
              <DataTable
                columns={['Branch', 'Last commit', 'Status']}
                rows={github.branches.map((branch) => [branch.name, branch.lastCommit, branch.status])}
              />
            </SectionCard>
            <SectionCard title="Commits" subtitle="Recent code changes">
              <div className="stack-list">
                {github.commits.map((commit) => (
                  <div className="list-item" key={commit.sha}>
                    <div>
                      <strong>{commit.message}</strong>
                      <div className="muted small">{commit.author}</div>
                    </div>
                    <div className="right-meta">
                      <code>{commit.sha}</code>
                      <span className="muted small">{commit.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </SectionCard>
          </div>
        </div>
      );
    }

    if (page === 'pipelines') {
      return (
        <div className="column-stack">
          <SectionCard title="Pipeline Runs" subtitle="Start pipeline, live logs, step timeline, test results, artifacts" action={<button className="primary" onClick={async () => { await api.startPipeline(); await loadData(); }}>Start pipeline</button>}>
            <div className="stack-list">
              {runs.map((run) => (
                <div key={run.id} className="pipeline-card">
                  <div className="pipeline-head">
                    <div>
                      <strong>{run.name}</strong>
                      <div className="muted small">{run.branch} · {run.commit} · {run.trigger}</div>
                    </div>
                    <Badge tone={run.status === 'Succeeded' ? 'success' : run.status === 'Failed' ? 'danger' : 'warning'}>{run.status}</Badge>
                  </div>
                  <div className="pipeline-grid">
                    <div>
                      <h4>Step timeline</h4>
                      {run.steps.map((step) => <div key={step.name} className="timeline-row"><span>{step.name}</span><span>{step.status} · {step.duration}</span></div>)}
                    </div>
                    <div>
                      <h4>Live logs</h4>
                      <pre className="log-box">{run.logs.join('\n')}</pre>
                    </div>
                    <div>
                      <h4>Test results</h4>
                      {run.testResults.map((test) => <div key={test.name} className="timeline-row"><span>{test.name}</span><Badge tone={test.status === 'passed' ? 'success' : 'danger'}>{test.status}</Badge></div>)}
                    </div>
                    <div>
                      <h4>Artifacts</h4>
                      {run.artifacts.map((artifact) => <div key={artifact} className="timeline-row"><span>{artifact}</span><span>download</span></div>)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      );
    }

    if (page === 'pulls') {
      return (
        <SectionCard title="Pull Requests" subtitle="Generated PRs, summaries, diff overview, and review status">
          <div className="stack-list">
            {prs.map((pr) => (
              <div className="list-item stretch" key={pr.id}>
                <div>
                  <strong>#{pr.id} {pr.title}</strong>
                  <div className="muted small">{pr.summary}</div>
                  <div className="chip-row">{pr.diffOverview.map((line) => <span className="chip" key={line}>{line}</span>)}</div>
                </div>
                <div className="right-meta align-top">
                  <Badge tone={pr.status === 'Merged' ? 'success' : 'info'}>{pr.status}</Badge>
                  <Badge tone={pr.reviewStatus === 'Approved' ? 'success' : pr.reviewStatus === 'Changes requested' ? 'danger' : 'warning'}>{pr.reviewStatus}</Badge>
                  <span className="muted small">+{pr.additions} / -{pr.deletions}</span>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>
      );
    }

    if (page === 'actions') {
      return (
        <div className="two-col">
          <SectionCard title="Workflow runs" subtitle="GitHub Actions status and retry links">
            <DataTable
              columns={['Workflow', 'Status', 'Failed jobs', 'Retry link']}
              rows={github.workflowRuns.map((workflow) => [workflow.name, workflow.status, String(workflow.failedJobs), workflow.retryUrl])}
            />
          </SectionCard>
          <SectionCard title="Failed jobs from pipelines" subtitle="Related logs and run statuses">
            <div className="stack-list">
              {runs.filter((run) => run.failedTests > 0).map((run) => (
                <div className="list-item" key={run.id}>
                  <div>
                    <strong>{run.name}</strong>
                    <div className="muted small">{run.failedTests} failed tests · {run.ticketKey}</div>
                  </div>
                  <Badge tone="danger">Needs retry</Badge>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      );
    }

    if (page === 'assistant') {
      return (
        <div className="two-col layout-wide">
          <SectionCard title="AI Assistant" subtitle="Ask project questions, get RAG-style answers, explain code, suggest fixes">
            <div className="form-grid">
              <textarea rows={5} value={assistantQuestion} onChange={(e) => setAssistantQuestion(e.target.value)} />
              <button className="primary" onClick={askAssistant}>Ask project question</button>
            </div>
            <div className="assistant-box">
              <h4>Answer</h4>
              <p>{assistantAnswer || 'Ask about pipelines, pull requests, Jira, code, or fixes.'}</p>
            </div>
          </SectionCard>
          <SectionCard title="Suggested prompts" subtitle="Examples for explain-code and fix recommendations">
            <div className="chip-row vertical">
              {[
                'Explain why the registration test is failing.',
                'Which pipeline should I retry next?',
                'Summarize open PRs and review blockers.',
                'What is slowing down Jira cycle time?',
              ].map((prompt) => (
                <button key={prompt} className="prompt-chip" onClick={() => setAssistantQuestion(prompt)}>{prompt}</button>
              ))}
            </div>
          </SectionCard>
        </div>
      );
    }

    if (page === 'reports') {
      return (
        <div className="two-col layout-wide">
          <SectionCard title="Pass / fail trends" subtitle="Recent test outcomes">
            <div className="chart-box">
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={reports.passFailTrends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="label" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="passed" strokeWidth={2} />
                  <Line type="monotone" dataKey="failed" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </SectionCard>
          <SectionCard title="Agent success rate" subtitle="Planner, code, test, and review agents">
            <div className="chart-box">
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie data={reports.agentSuccessRate} dataKey="value" nameKey="name" outerRadius={100} />
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </SectionCard>
          <SectionCard title="Jira cycle time" subtitle="Average days spent per status">
            <DataTable
              columns={['Status', 'Avg days']}
              rows={reports.jiraCycleTime.map((item) => [item.name, String(item.days)])}
            />
          </SectionCard>
          <SectionCard title="PR throughput" subtitle="Weekly merged and ready PR volume">
            <div className="chart-box">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={reports.prThroughput}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="label" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" radius={[10, 10, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </SectionCard>
        </div>
      );
    }

    return (
      <div className="two-col">
        {Object.entries(settings).map(([name, config]) => (
          <SectionCard key={name} title={name === 'vectorDb' ? 'Vector DB settings' : `${name} settings`} subtitle="Connection and provider info">
            <div className="detail-grid">
              {Object.entries(config).map(([label, value]) => <InfoRow key={label} label={label} value={String(value)} />)}
            </div>
          </SectionCard>
        ))}
      </div>
    );
  }, [assistantAnswer, assistantQuestion, dashboard, github, loading, page, reports, settings, ticketForm]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><FolderGit2 size={20} /> AI DevOps Platform</div>
        <nav className="nav-list">
          {NAV.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.key} className={`nav-item ${page === item.key ? 'active' : ''}`} onClick={() => setPage(item.key as PageKey)}>
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>
      <main className="content">
        <div className="topbar">
          <div>
            <div className="eyebrow">Mahdi20202 / AI-DevOps-Pipeline</div>
            <h2>{NAV.find((item) => item.key === page)?.label}</h2>
          </div>
          <button className="secondary" onClick={loadData}>Refresh data</button>
        </div>
        {content}
      </main>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="info-row">
      <span className="muted">{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function DataTable({ columns, rows }: { columns: string[]; rows: string[][] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row, index) => <tr key={index}>{row.map((cell, i) => <td key={`${index}-${i}`}>{cell}</td>)}</tr>)}
        </tbody>
      </table>
    </div>
  );
}

export default App;
