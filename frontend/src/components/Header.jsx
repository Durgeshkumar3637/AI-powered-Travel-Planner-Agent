import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-lg font-bold text-slate-800">
          <span className="text-2xl">✈️</span> Travel Planner Agent
        </Link>
        <nav className="flex items-center gap-4 text-sm font-medium text-slate-600">
          <Link to="/" className="hover:text-sky-600">Home</Link>
          <Link to="/plan" className="hover:text-sky-600">Plan Trip</Link>
        </nav>
      </div>
    </header>
  )
}
