import { useState } from 'react'
import { chat } from '../services/api.js'

export default function AIChat({ plan, tripRequest }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const send = async (e) => {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return
    setInput('')
    setMessages((m) => [...m, { role: 'user', text: question }])
    setLoading(true)
    try {
      const res = await chat(question, plan, tripRequest)
      setMessages((m) => [...m, { role: 'ai', text: res.answer }])
    } catch {
      setMessages((m) => [...m, { role: 'ai', text: 'Sorry, the AI assistant is unavailable right now. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <h3 className="mb-3 text-lg font-bold text-slate-800">🤖 AI Travel Assistant</h3>
      <div className="mb-4 max-h-64 space-y-3 overflow-y-auto">
        {messages.length === 0 && (
          <p className="text-sm text-slate-400">Ask anything about your trip, e.g. "Make my trip cheaper."</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`rounded-xl px-4 py-2 text-sm ${
            m.role === 'user' ? 'ml-8 bg-sky-500 text-white' : 'mr-8 bg-slate-100 text-slate-700'
          }`}>
            {m.text}
          </div>
        ))}
        {loading && <p className="text-sm text-slate-400">IBM Granite is thinking…</p>}
      </div>
      <form onSubmit={send} className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your trip..."
          className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none"
        />
        <button type="submit" disabled={loading}
          className="rounded-lg bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700 disabled:opacity-60">
          Send
        </button>
      </form>
    </div>
  )
}
