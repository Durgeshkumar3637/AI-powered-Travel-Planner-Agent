import { useState } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import BudgetCard from '../components/BudgetCard.jsx'
import Itinerary from '../components/Itinerary.jsx'
import WeatherCard from '../components/WeatherCard.jsx'
import HotelCard from '../components/HotelCard.jsx'
import TransportCard from '../components/TransportCard.jsx'
import AIChat from '../components/AIChat.jsx'
import { replanTrip } from '../services/api.js'

const fmt = (n) => `₹${Number(n).toLocaleString('en-IN')}`

export default function TripResult() {
  const location = useLocation()
  const navigate = useNavigate()
  const [result, setResult] = useState(location.state)
  const [instruction, setInstruction] = useState('')
  const [replanning, setReplanning] = useState(false)
  const [error, setError] = useState('')

  if (!result?.plan) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-20 text-center">
        <p className="text-lg text-slate-600">No trip plan found.</p>
        <Link to="/plan" className="mt-4 inline-block rounded-xl bg-sky-600 px-6 py-3 font-semibold text-white hover:bg-sky-700">
          Plan a Trip
        </Link>
      </div>
    )
  }

  const { plan, trip_request: req } = result
  const days = result.days || plan.itinerary.length

  const modify = async (e) => {
    e.preventDefault()
    const text = instruction.trim()
    if (!text || replanning) return
    setReplanning(true)
    setError('')
    try {
      const updated = await replanTrip(text, plan, req)
      setResult(updated)
      setInstruction('')
    } catch (err) {
      setError(err.message || 'Unable to modify your trip right now.')
    } finally {
      setReplanning(false)
    }
  }

  return (
    <div className="mx-auto max-w-6xl space-y-8 px-4 py-10">
      {/* Header */}
      <div className="rounded-2xl bg-gradient-to-r from-sky-600 to-indigo-600 p-8 text-white shadow">
        <h1 className="text-3xl font-extrabold">{req.origin} → {req.destination}</h1>
        <p className="mt-2 text-sky-100">
          {days} Days | {req.travellers} Traveller{req.travellers > 1 ? 's' : ''} | {req.travel_style}
        </p>
        <div className="mt-4 flex flex-wrap gap-6">
          <div><p className="text-xs text-sky-200">Budget</p><p className="text-xl font-bold">{fmt(req.budget)}</p></div>
          <div><p className="text-xs text-sky-200">Estimated Cost</p><p className="text-xl font-bold">{fmt(plan.estimated_budget.total)}</p></div>
        </div>
      </div>

      {/* Summary */}
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <h3 className="mb-2 text-lg font-bold text-slate-800">🧳 Your Trip</h3>
        <p className="text-slate-600">{plan.trip_summary}</p>
      </div>

      {/* Budget + Weather */}
      <div className="grid gap-8 lg:grid-cols-2">
        <BudgetCard
          budget={req.budget}
          plan={plan}
          overBudget={result.over_budget}
          remaining={result.remaining}
          savingsSuggestions={result.savings_suggestions}
        />
        <WeatherCard destination={req.destination} />
      </div>

      {/* Itinerary */}
      <Itinerary itinerary={plan.itinerary} />

      {/* Hotels + Transport */}
      <HotelCard accommodation={plan.accommodation} />
      <TransportCard transportation={plan.transportation} origin={req.origin} destination={req.destination} />

      {/* Tips */}
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <h3 className="mb-3 text-lg font-bold text-slate-800">💡 Travel Tips</h3>
        <ul className="grid gap-2 sm:grid-cols-2">
          {plan.tips.map((tip, i) => (
            <li key={i} className="rounded-lg bg-amber-50 px-4 py-2 text-sm text-amber-900">✓ {tip}</li>
          ))}
        </ul>
      </div>

      {/* Replan + Chat */}
      <div className="grid gap-8 lg:grid-cols-2">
        <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <h3 className="mb-1 text-lg font-bold text-slate-800">✏️ Modify My Trip</h3>
          <p className="mb-3 text-sm text-slate-500">e.g. "Make Day 3 more relaxed." or "Reduce my budget to ₹30,000."</p>
          <form onSubmit={modify} className="flex gap-2">
            <input
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              placeholder="How would you like to change your trip?"
              className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none"
            />
            <button type="submit" disabled={replanning}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60">
              {replanning ? 'Updating…' : 'Update Plan'}
            </button>
          </form>
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
          {result.change_applied && !replanning && (
            <p className="mt-2 text-sm text-emerald-600">✓ Applied: "{result.change_applied}"</p>
          )}
        </div>
        <AIChat plan={plan} tripRequest={req} />
      </div>
    </div>
  )
}
