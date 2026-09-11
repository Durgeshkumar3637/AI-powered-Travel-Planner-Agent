export default function BudgetCard({ budget, plan, overBudget, remaining, savingsSuggestions = [] }) {
  const b = plan.estimated_budget
  const fmt = (n) => `₹${Number(n).toLocaleString('en-IN')}`
  const rows = [
    ['Transportation', b.transportation],
    ['Accommodation', b.accommodation],
    ['Food', b.food],
    ['Activities', b.activities],
    ['Local Transport', b.local_transport],
    ['Miscellaneous', b.miscellaneous],
  ]
  const pct = budget > 0 ? Math.min(100, (b.total / budget) * 100) : 100

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <h3 className="mb-4 text-lg font-bold text-slate-800">💰 Estimated Budget</h3>
      <div className="space-y-2">
        {rows.map(([k, v]) => (
          <div key={k} className="flex justify-between text-sm text-slate-600">
            <span>{k}</span><span className="font-medium text-slate-800">{fmt(v)}</span>
          </div>
        ))}
        <div className="flex justify-between border-t border-slate-200 pt-2 font-bold text-slate-800">
          <span>Total</span><span>{fmt(b.total)}</span>
        </div>
      </div>

      <div className="mt-5">
        <div className="mb-1 flex justify-between text-xs text-slate-500">
          <span>User Budget: {fmt(budget)}</span><span>{Math.round(pct)}% used</span>
        </div>
        <div className="h-3 overflow-hidden rounded-full bg-slate-100">
          <div className={`h-full rounded-full ${overBudget ? 'bg-red-500' : 'bg-emerald-500'}`} style={{ width: `${pct}%` }} />
        </div>
        <p className={`mt-2 text-sm font-medium ${overBudget ? 'text-red-600' : 'text-emerald-600'}`}>
          {overBudget
            ? `Your estimated trip cost exceeds your budget by ${fmt(-remaining)}.`
            : `Remaining: ${fmt(remaining)}`}
        </p>
      </div>

      {overBudget && savingsSuggestions.length > 0 && (
        <div className="mt-4 rounded-lg bg-amber-50 p-4">
          <p className="mb-2 text-sm font-semibold text-amber-800">💡 Cost-Saving Suggestions</p>
          <ul className="list-disc space-y-1 pl-4 text-sm text-amber-800">
            {savingsSuggestions.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}
    </div>
  )
}
