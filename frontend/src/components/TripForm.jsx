import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { planTrip } from '../services/api.js'

const INTERESTS = ['Beaches', 'Nature', 'Historical Places', 'Food', 'Shopping', 'Adventure', 'Culture', 'Nightlife', 'Photography', 'Sightseeing']
const STYLES = ['Budget', 'Standard', 'Luxury', 'Family', 'Couple', 'Adventure', 'Relaxation']

export default function TripForm() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    origin: 'Delhi',
    destination: 'Goa',
    start_date: '',
    end_date: '',
    travellers: 2,
    budget: 40000,
    currency: 'INR',
    travel_style: 'Couple',
    interests: ['Beaches', 'Food', 'Sightseeing'],
    preferences: 'I prefer a relaxed trip and do not want too much walking.',
  })

  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const toggleInterest = (i) => {
    setForm({
      ...form,
      interests: form.interests.includes(i)
        ? form.interests.filter((x) => x !== i)
        : [...form.interests, i],
    })
  }

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    if (!form.start_date || !form.end_date) return setError('Please select travel dates.')
    if (form.end_date < form.start_date) return setError('End date must be after the start date.')
    if (!form.budget || Number(form.budget) <= 0) return setError('Please enter a valid budget.')
    if (!form.interests.length) return setError('Please select at least one interest.')
    setLoading(true)
    try {
      const result = await planTrip({ ...form, travellers: Number(form.travellers), budget: Number(form.budget) })
      navigate('/trip', { state: result })
    } catch (err) {
      setError(err.message || 'Unable to generate your trip right now. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const input = 'w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none'
  const label = 'mb-1 block text-sm font-medium text-slate-700'

  return (
    <form onSubmit={submit} className="space-y-5">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className={label}>Starting Location</label>
          <input className={input} value={form.origin} onChange={set('origin')} placeholder="Delhi" required />
        </div>
        <div>
          <label className={label}>Destination</label>
          <input className={input} value={form.destination} onChange={set('destination')} placeholder="Goa" required />
        </div>
        <div>
          <label className={label}>Start Date</label>
          <input type="date" className={input} value={form.start_date} onChange={set('start_date')} required />
        </div>
        <div>
          <label className={label}>End Date</label>
          <input type="date" className={input} value={form.end_date} onChange={set('end_date')} required />
        </div>
        <div>
          <label className={label}>Number of Travellers</label>
          <input type="number" min="1" max="20" className={input} value={form.travellers} onChange={set('travellers')} required />
        </div>
        <div>
          <label className={label}>Budget</label>
          <input type="number" min="0" className={input} value={form.budget} onChange={set('budget')} required />
        </div>
        <div>
          <label className={label}>Currency</label>
          <select className={input} value={form.currency} onChange={set('currency')}>
            <option>INR</option><option>USD</option><option>EUR</option>
          </select>
        </div>
        <div>
          <label className={label}>Travel Style</label>
          <select className={input} value={form.travel_style} onChange={set('travel_style')}>
            {STYLES.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
      </div>

      <div>
        <label className={label}>Interests</label>
        <div className="flex flex-wrap gap-2">
          {INTERESTS.map((i) => (
            <button type="button" key={i} onClick={() => toggleInterest(i)}
              className={`rounded-full border px-3 py-1 text-sm transition ${
                form.interests.includes(i)
                  ? 'border-sky-500 bg-sky-500 text-white'
                  : 'border-slate-300 bg-white text-slate-600 hover:border-sky-400'
              }`}>
              {i}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className={label}>Additional Preferences</label>
        <textarea className={input} rows="3" value={form.preferences} onChange={set('preferences')}
          placeholder="I prefer a relaxed trip and don't want too much walking." />
      </div>

      {error && <p className="rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>}

      <button type="submit" disabled={loading}
        className="w-full rounded-lg bg-sky-600 py-3 font-semibold text-white transition hover:bg-sky-700 disabled:opacity-60">
        {loading ? '✨ IBM Granite is planning your trip...' : 'Generate Travel Plan'}
      </button>
    </form>
  )
}
