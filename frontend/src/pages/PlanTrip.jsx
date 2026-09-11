import TripForm from '../components/TripForm.jsx'

export default function PlanTrip() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="mb-2 text-3xl font-extrabold text-slate-800">Plan Your Trip</h1>
      <p className="mb-8 text-slate-500">Fill in your travel details and let IBM Granite do the rest.</p>
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200 sm:p-8">
        <TripForm />
      </div>
    </div>
  )
}
