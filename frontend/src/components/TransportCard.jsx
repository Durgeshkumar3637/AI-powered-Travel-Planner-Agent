export default function TransportCard({ transportation, origin, destination }) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <h3 className="mb-1 text-lg font-bold text-slate-800">🚗 Transportation Suggestions</h3>
      <p className="mb-4 text-xs text-amber-600">Estimated costs only — no actual bookings are made.</p>
      <p className="mb-3 text-sm font-medium text-slate-700">{origin} → {destination}</p>
      <div className="space-y-3">
        {transportation.map((t, i) => (
          <div key={i} className="flex items-center justify-between rounded-xl bg-slate-50 p-4">
            <div>
              <p className="font-semibold text-slate-800">🚄 {t.mode}</p>
              <p className="text-xs text-slate-500">{t.description}</p>
            </div>
            <span className="font-medium text-slate-700">
              ₹{Number(t.estimated_cost).toLocaleString('en-IN')}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
