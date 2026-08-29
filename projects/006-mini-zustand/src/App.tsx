import { IssueList } from './components/IssueList'
import { SearchBox } from './components/SearchBox'
import { SelectionPanel } from './components/SelectionPanel'
import { StatusFilter } from './components/StatusFilter'
import './styles.css'

export function App() {
  return (
    <main>
      <header>
        <div className="brand">MZ</div>
        <div><p className="eyebrow">Practice project #6</p><h1>Mini Zustand <em>Lab</em></h1></div>
        <span className="framework-pill">React external store</span>
      </header>

      <section className="intro">
        <p className="eyebrow">The experiment</p>
        <h2>Change one slice.<br /><span>Watch what renders.</span></h2>
        <p>The counters make subscriptions visible. Selecting an issue should not rerender the search or filter controls.</p>
      </section>

      <div className="workspace">
        <div className="controls"><SearchBox /><StatusFilter /><SelectionPanel /></div>
        <IssueList />
      </div>

      <footer><span>state change</span><b>→</b><span>listener</span><b>→</b><span>React snapshot</span><b>→</b><span>selected render</span></footer>
    </main>
  )
}
