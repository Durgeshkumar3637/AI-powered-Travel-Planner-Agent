import { useEffect, useState } from 'react'
import { getWeather } from '../services/api.js'

export default function WeatherCard({ destination }) {
  const [weather, setWeather] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    getWeather(destination)
      .then((w) => active && setWeather(w))
      .catch(() => active && setError('Weather information is unavailable right now.'))
    return () => { active = false }
  }, [destination])

  if (error) {
    return (
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <h3 className="mb-2 text-lg font-bold text-slate-800">🌤️ Weather</h3>
        <p className="text-sm text-slate-500">{error}</p>
      </div>
    )
  }
  if (!weather) {
    return (
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <p className="text-sm text-slate-400">Loading weather…</p>
      </div>
    )
  }

  return (
    <div className="rounded-2xl bg-gradient-to-br from-sky-500 to-indigo-500 p-6 text-white shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-lg font-bold">🌤️ Weather — {weather.destination}</h3>
        {weather.source === 'demo' && (
          <span className="rounded-full bg-white/20 px-3 py-1 text-xs font-medium">Demo Weather Data</span>
        )}
      </div>
      <div className="grid grid-cols-3 gap-4 text-center">
        <div>
          <p className="text-3xl font-bold">{weather.temperature}°C</p>
          <p className="text-xs text-sky-100">Temperature</p>
        </div>
        <div>
          <p className="text-lg font-semibold capitalize">{weather.condition}</p>
          <p className="text-xs text-sky-100">Condition</p>
        </div>
        <div>
          <p className="text-lg font-semibold">{weather.rain_probability}%</p>
          <p className="text-xs text-sky-100">Rain Probability</p>
        </div>
      </div>
      <p className="mt-3 text-xs text-sky-100">Humidity: {weather.humidity}%</p>
    </div>
  )
}
