'use client'
import { supabase } from '@/lib/supabase'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, Target } from 'lucide-react'

type InterviewRow = {
  session_id: string
  scheduled_at: string
  round_type: string
  score: number | null
  feedback: string | null
}

export default function InterviewPage() {
  const [rows, setRows] = useState<InterviewRow[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      setLoading(true)
      const { data: { session } } = await supabase.auth.getSession()
      const uid = session?.user?.id
      if (!uid) return

      const { data, error } = await supabase
        .from('interview_sessions')
        .select('session_id, scheduled_at, round_type, score, feedback')
        .eq('user_id', uid)
        .order('scheduled_at', { ascending: false })

      if (error) console.error(error)
      setRows((data ?? []) as any)
      setLoading(false)
    }
    run()
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-6xl mx-auto">
        <Link href="/dashboard" className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900">
          <ArrowLeft className="w-4 h-4" /> Back
        </Link>

        <div className="mt-4 bg-white border border-slate-200 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-slate-700" />
            <h1 className="text-xl font-bold text-slate-900">Interview Prep</h1>
          </div>

          {loading ? (
            <p className="text-slate-600">Loading…</p>
          ) : rows.length === 0 ? (
            <p className="text-slate-600">No interview sessions yet.</p>
          ) : (
            <div className="space-y-3">
              {rows.map((r) => (
                <div key={r.session_id} className="border border-slate-200 rounded-2xl p-5 bg-slate-50">
                  <p className="font-semibold text-slate-900">{r.round_type}</p>
                  <p className="text-sm text-slate-600 mt-1">
                    Scheduled: {new Date(r.scheduled_at).toLocaleString()}
                  </p>
                  <p className="text-sm text-slate-600 mt-1">Score: {r.score ?? '—'}</p>
                  {r.feedback ? (
                    <p className="text-sm text-slate-700 mt-3 whitespace-pre-wrap">{r.feedback}</p>
                  ) : null}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
