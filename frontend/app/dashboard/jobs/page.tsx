'use client'
import { supabase } from '@/lib/supabase'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, Briefcase, Star } from 'lucide-react'

type JobMatch = {
  match_id: string
  job_title: string
  company: string
  match_score: number
  status: string
  created_at: string
}

export default function JobsPage() {
  const [rows, setRows] = useState<JobMatch[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      setLoading(true)
      const { data: { session } } = await supabase.auth.getSession()
      const uid = session?.user?.id
      if (!uid) return

      const { data, error } = await supabase
        .from('job_matches')
        .select('match_id, job_title, company, match_score, status, created_at')
        .eq('user_id', uid)
        .order('created_at', { ascending: false })

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
            <Briefcase className="w-5 h-5 text-slate-700" />
            <h1 className="text-xl font-bold text-slate-900">Job Matches</h1>
          </div>

          {loading ? (
            <p className="text-slate-600">Loading…</p>
          ) : rows.length === 0 ? (
            <p className="text-slate-600">No job matches yet.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-500 border-b">
                    <th className="py-3">Role</th>
                    <th>Company</th>
                    <th>Score</th>
                    <th>Status</th>
                    <th className="text-right">Created</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r) => (
                    <tr key={r.match_id} className="border-b last:border-b-0">
                      <td className="py-3 font-medium text-slate-900">{r.job_title}</td>
                      <td className="text-slate-700">{r.company}</td>
                      <td className="text-slate-700 inline-flex items-center gap-1">
                        <Star className="w-4 h-4" /> {r.match_score}
                      </td>
                      <td className="text-slate-700">{r.status}</td>
                      <td className="text-right text-slate-500">{new Date(r.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
