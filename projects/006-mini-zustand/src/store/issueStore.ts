import { createStore } from './createStore'

export type IssueStatus = 'open' | 'done'

export interface Issue {
  id: number
  title: string
  status: IssueStatus
  description: string
}

export interface IssueState {
  issues: Issue[]
  search: string
  statusFilter: 'all' | IssueStatus
  selectedIssueId: number | null
}

export const issueStore = createStore<IssueState>({
  issues: [
    { id: 32, title: 'Authentication bug', status: 'open', description: 'Refresh tokens fail after returning to the app.' },
    { id: 41, title: 'Improve caching', status: 'open', description: 'Avoid duplicate requests for issue details.' },
    { id: 52, title: 'Fix dashboard', status: 'done', description: 'Correct the mobile dashboard layout.' },
    { id: 67, title: 'Document selectors', status: 'done', description: 'Explain selector identity and equality.' },
  ],
  search: '',
  statusFilter: 'all',
  selectedIssueId: null,
})
