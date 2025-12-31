'use client'
import { supabase } from '@/lib/supabase'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, FileText } from 'lucide-react'

type AppRow = {
  application_id: string
  company: string
  job_title: string
  status: string
  applied_on: string
}

export default function ApplicationsPage() {
  const [rows, setRows] = useState<AppRow[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      setLoading(true)
      const { data: { session } } = await supabase.auth.getSession()
      const uid = session?.user?.id
      if (!uid) return

      const { data, error } = await supabase
        .from('applications')
        .select('id, company, job_title, status, applied_on')
        .eq('user_id', uid)
        .order('applied_on', { ascending: false })

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
            <FileText className="w-5 h-5 text-slate-700" />
            <h1 className="text-xl font-bold text-slate-900">Applications</h1>
          </div>

          {loading ? (
            <p className="text-slate-600">Loading…</p>
          ) : rows.length === 0 ? (
            <p className="text-slate-600">No applications yet.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-500 border-b">
                    <th className="py-3">Role</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th className="text-right">Applied</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r) => (
                    <tr key={r.application_id} className="border-b last:border-b-0">
                      <td className="py-3 font-medium text-slate-900">{r.job_title}</td>
                      <td className="text-slate-700">{r.company}</td>
                      <td className="text-slate-700">{r.status}</td>
                      <td className="text-right text-slate-500">{new Date(r.applied_on).toLocaleDateString()}</td>
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
