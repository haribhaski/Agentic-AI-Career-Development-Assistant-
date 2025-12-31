'use client'
import { supabase } from '@/lib/supabase'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, GraduationCap } from 'lucide-react'

type LearningRow = {
  id: string
  skill: string
  current_level: number
  target_level: number
  hours_completed: number
  updated_at: string
}

export default function LearningPage() {
  const [rows, setRows] = useState<LearningRow[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      setLoading(true)
      const { data: { session } } = await supabase.auth.getSession()
      const uid = session?.user?.id
      if (!uid) return

      const { data, error } = await supabase
        .from('learning_progress')
        .select('id, skill, current_level, target_level, hours_completed, updated_at')
        .eq('user_id', uid)
        .order('updated_at', { ascending: false })

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
            <GraduationCap className="w-5 h-5 text-slate-700" />
            <h1 className="text-xl font-bold text-slate-900">Learning Progress</h1>
          </div>

          {loading ? (
            <p className="text-slate-600">Loading…</p>
          ) : rows.length === 0 ? (
            <p className="text-slate-600">No learning progress yet.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {rows.map((r) => (
                <div key={r.id} className="border border-slate-200 rounded-2xl p-5 bg-slate-50">
                  <p className="font-semibold text-slate-900">{r.skill}</p>
                  <p className="text-sm text-slate-600 mt-1">
                    Level {r.current_level} → {r.target_level}
                  </p>
                  <p className="text-sm text-slate-600 mt-1">Hours: {r.hours_completed}</p>
                  <p className="text-xs text-slate-500 mt-3">
                    Updated {new Date(r.updated_at).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
