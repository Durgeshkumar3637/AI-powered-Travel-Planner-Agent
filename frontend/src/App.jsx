import { Routes, Route } from 'react-router-dom'
import Header from './components/Header.jsx'
import Home from './pages/Home.jsx'
import PlanTrip from './pages/PlanTrip.jsx'
import TripResult from './pages/TripResult.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/plan" element={<PlanTrip />} />
          <Route path="/trip" element={<TripResult />} />
        </Routes>
      </main>
      <footer className="border-t border-slate-200 bg-white py-6 text-center text-sm text-slate-500">
        Travel Planner Agent · Powered by IBM Granite + IBM Cloud
      </footer>
    </div>
  )
}
