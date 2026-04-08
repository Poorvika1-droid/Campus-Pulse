import { FormEvent, useState } from 'react'
import { askAssistant } from '../lib/api'

export function AssistantPanel() {
  const [question, setQuestion] = useState('Where should I go now?')
  const [answer, setAnswer] = useState('')
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await askAssistant(question)
      setAnswer(res.answer)
      setSuggestions(res.suggestions)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <h2>AI Campus Assistant</h2>
      <form onSubmit={onSubmit} className="assistant-form">
        <input value={question} onChange={(e) => setQuestion(e.target.value)} />
        <button type="submit" disabled={loading}>{loading ? 'Thinking...' : 'Ask'}</button>
      </form>
      {answer && <p className="answer">{answer}</p>}
      <ul>
        {suggestions.map((s) => <li key={s}>{s}</li>)}
      </ul>
    </section>
  )
}
