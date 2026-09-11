const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function handle(res) {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.detail || 'Something went wrong. Please try again.')
  }
  return data
}

export async function planTrip(payload) {
  return handle(await fetch(`${BASE}/api/plan-trip`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }))
}

export async function chat(question, plan, tripRequest) {
  return handle(await fetch(`${BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, trip: plan, trip_request: tripRequest }),
  }))
}

export async function replanTrip(instruction, plan, tripRequest) {
  return handle(await fetch(`${BASE}/api/replan-trip`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ instruction, trip: plan, trip_request: tripRequest }),
  }))
}

export async function getWeather(destination) {
  return handle(await fetch(`${BASE}/api/weather?destination=${encodeURIComponent(destination)}`))
}

export async function getHealth() {
  return handle(await fetch(`${BASE}/api/health`))
}
