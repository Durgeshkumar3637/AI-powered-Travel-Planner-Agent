export default function HotelCard({ accommodation }) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <h3 className="mb-1 text-lg font-bold text-slate-800">🏨 Accommodation Suggestions</h3>
      <p className="mb-4 text-xs text-amber-600">AI-generated estimates — verify availability before booking.</p>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {accommodation.map((h, i) => (
          <div key={i} className="rounded-xl bg-slate-50 p-4">
            <span className="mb-2 inline-block rounded-full bg-sky-100 px-2 py-0.5 text-xs font-semibold text-sky-700">
              {h.type}
            </span>
            <h4 className="font-semibold text-slate-800">{h.name}</h4>
            <p className="mt-1 text-sm font-medium text-slate-700">
              ₹{Number(h.estimated_price_per_night).toLocaleString('en-IN')}/night
            </p>
            {h.location && <p className="text-xs text-slate-500">📍 {h.location}</p>}
            {h.why && <p className="mt-2 text-xs text-slate-600">{h.why}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}
