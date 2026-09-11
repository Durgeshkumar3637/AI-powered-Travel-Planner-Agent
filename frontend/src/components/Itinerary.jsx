export default function Itinerary({ itinerary }) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <h3 className="mb-6 text-lg font-bold text-slate-800">🗓️ Day-by-Day Itinerary</h3>
      <div className="space-y-8">
        {itinerary.map((day) => (
          <div key={day.day} className="relative border-l-2 border-sky-200 pl-6">
            <span className="absolute -left-[9px] top-1 flex h-4 w-4 items-center justify-center rounded-full bg-sky-500 ring-4 ring-sky-100" />
            <div className="mb-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-sky-600">Day {day.day}</p>
              <h4 className="text-lg font-bold text-slate-800">{day.title}</h4>
            </div>
            <div className="space-y-3">
              {day.activities?.map((a, i) => (
                <div key={i} className="rounded-lg bg-slate-50 p-3 sm:flex sm:items-center sm:justify-between sm:gap-4">
                  <div className="sm:flex sm:flex-1 sm:items-center sm:gap-4">
                    <span className="inline-block min-w-[72px] text-sm font-semibold text-sky-700">{a.time}</span>
                    <div>
                      <p className="text-sm font-medium text-slate-800">{a.activity}</p>
                      {a.location && <p className="text-xs text-slate-500">📍 {a.location}</p>}
                    </div>
                  </div>
                  <span className="mt-1 inline-block text-xs text-slate-500 sm:mt-0">
                    {a.estimated_cost > 0 ? `₹${Number(a.estimated_cost).toLocaleString('en-IN')}` : 'Free'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
