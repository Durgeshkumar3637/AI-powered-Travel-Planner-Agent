import { Link } from 'react-router-dom'

const FEATURES = [
  ['🧠', 'AI-Powered Planning', 'IBM Granite analyzes your preferences to build the perfect plan.'],
  ['🗺️', 'Personalized Itinerary', 'A day-by-day schedule with places, times and activities.'],
  ['💰', 'Budget Estimation', 'A clear cost breakdown that fits your budget.'],
  ['🌤️', 'Weather Information', 'Know the weather before you travel.'],
]

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-sky-500 via-sky-600 to-indigo-600 text-white">
        <div className="mx-auto max-w-6xl px-4 py-20 text-center">
          <h1 className="text-4xl font-extrabold sm:text-5xl">Travel Planner Agent</h1>
          <p className="mt-3 text-xl text-sky-100">Plan your perfect trip with AI</p>
          <p className="mx-auto mt-4 max-w-2xl text-sky-100">
            Tell us where you want to go, your budget, interests, and travel preferences.
            IBM Granite will create a personalized travel itinerary for you.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link to="/plan" className="rounded-xl bg-white px-6 py-3 font-semibold text-sky-700 shadow hover:bg-sky-50">
              Plan My Trip
            </Link>
            <a href="#how-it-works" className="rounded-xl border border-white/40 px-6 py-3 font-semibold hover:bg-white/10">
              How It Works
            </a>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-6xl px-4 py-16">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {FEATURES.map(([icon, title, desc]) => (
            <div key={title} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
              <div className="mb-3 text-3xl">{icon}</div>
              <h3 className="mb-1 font-bold text-slate-800">{title}</h3>
              <p className="text-sm text-slate-500">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="bg-white py-16">
        <div className="mx-auto max-w-3xl px-4">
          <h2 className="mb-8 text-center text-2xl font-bold text-slate-800">How It Works</h2>
          <ol className="space-y-5">
            {[
              'Enter your trip details — origin, destination, dates, budget and interests.',
              'IBM Granite understands your preferences and generates a personalized itinerary.',
              'The backend calculates your estimated budget and fetches weather information.',
              'View your complete travel dashboard, chat with the AI assistant, or modify your trip.',
            ].map((step, i) => (
              <li key={i} className="flex items-start gap-4 rounded-xl bg-slate-50 p-4">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-sky-500 font-bold text-white">{i + 1}</span>
                <p className="text-slate-700">{step}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* Powered by */}
      <section className="mx-auto max-w-6xl px-4 pb-16 text-center">
        <div className="rounded-2xl bg-slate-900 px-6 py-8 text-white">
          <p className="text-sm uppercase tracking-widest text-slate-400">Powered by</p>
          <p className="mt-2 text-xl font-bold">IBM Granite <span className="text-slate-500">+</span> IBM Cloud</p>
          <p className="mt-2 text-sm text-slate-400">IBM Granite is the primary AI model used by the Travel Planner Agent.</p>
        </div>
      </section>
    </div>
  )
}
