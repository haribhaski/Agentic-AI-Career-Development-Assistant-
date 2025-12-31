'use client'

import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import { useEffect, useMemo, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Send,
  Sparkles,
  Briefcase,
  BookOpen,
  Target,
  Award,
  ChevronRight,
  Plus,
  LogOut,
  Menu,
  Home,
  FileText,
  GraduationCap,
  Activity,
  RefreshCw,
} from 'lucide-react'

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

type DashboardRow = {
  user_id: string
  total_job_matches: number | null
  avg_match_score: number | null
  skills_learning: number | null
  total_learning_hours: number | null
  applications_sent: number | null
  interviews_completed: number | null
  last_updated: string | null
}

const makeEmptyDash = (userId: string): DashboardRow => ({
  user_id: userId,
  total_job_matches: 0,
  avg_match_score: 0,
  skills_learning: 0,
  total_learning_hours: 0,
  applications_sent: 0,
  interviews_completed: 0,
  last_updated: null,
})

export default function DashboardPage() {
  const router = useRouter()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const [userId, setUserId] = useState<string | null>(null)
  const [userEmail, setUserEmail] = useState<string | null>(null)

  const [sidebarOpen, setSidebarOpen] = useState(true)

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content:
        "👋 Hey! I'm your AI career companion. Ask me to match jobs, build a learning path, improve your resume, or prep for interviews.",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  const [dash, setDash] = useState<DashboardRow | null>(null)
  const [learningHours, setLearningHours] = useState<number>(0)
  const [loadingStats, setLoadingStats] = useState(true)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  // Auth guard + set user
  useEffect(() => {
    let mounted = true
    supabase.auth.getSession().then(({ data }) => {
      if (!mounted) return
      const session = data.session
      if (!session) {
        router.push('/')
        return
      }
      setUserId(session.user.id)
      setUserEmail(session.user.email ?? null)
    })
    return () => {
      mounted = false
    }
  }, [router])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/')
  }

  const loadStats = async () => {
    if (!userId) return
    setLoadingStats(true)

    try {
      // ✅ 1) Dashboard view: use maybeSingle so "0 rows" doesn't throw
      const { data: dashRow, error: dashErr } = await supabase
        .from('user_career_dashboard')
        .select('*')
        .eq('user_id', userId)
        .maybeSingle()

      if (dashErr) {
        console.error(
          'Dashboard view error:',
          dashErr.message,
          (dashErr as any).code,
          (dashErr as any).details
        )
      }

      // ✅ ALWAYS set dash to something so UI never gets stuck or crashes
      setDash((dashRow as DashboardRow) ?? makeEmptyDash(userId))

      // ✅ 2) learning hours (optional)
      // If your view already returns total_learning_hours correctly,
      // you can delete this whole block.
      const { data: lpRows, error: lpErr } = await supabase
        .from('learning_progress')
        .select('hours_completed')
        .eq('user_id', userId)

      if (lpErr) {
        console.error('Learning hours error:', lpErr.message, (lpErr as any).code)
        setLearningHours(0)
      } else {
        const total = (lpRows ?? []).reduce((s, r: any) => s + (r.hours_completed ?? 0), 0)
        setLearningHours(total)
      }
    } catch (e) {
      console.error('loadStats crashed:', e)
      // fallback
      setDash(makeEmptyDash(userId))
      setLearningHours(0)
    } finally {
      setLoadingStats(false)
    }
  }

  useEffect(() => {
    if (userId) loadStats()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId])

  const stats = useMemo(() => {
    const d = dash ?? makeEmptyDash(userId ?? 'unknown')

    return [
      { label: 'Skills Tracked', value: String(d.skills_learning ?? 0), icon: Award, color: 'text-blue-600', bg: 'bg-blue-50' },
      { label: 'Jobs Matched', value: String(d.total_job_matches ?? 0), icon: Briefcase, color: 'text-green-600', bg: 'bg-green-50' },
      // Use view total if present; else fallback to computed
      { label: 'Learning Hours', value: String(d.total_learning_hours ?? learningHours ?? 0), icon: BookOpen, color: 'text-purple-600', bg: 'bg-purple-50' },
      { label: 'Applications', value: String(d.applications_sent ?? 0), icon: Target, color: 'text-orange-600', bg: 'bg-orange-50' },
    ]
  }, [dash, learningHours, userId])

  const quickActions = [
    { icon: Briefcase, label: 'Find Jobs', preset: 'Find job matches for my profile and suggest next steps.' },
    { icon: BookOpen, label: 'Learning Path', preset: 'Create a 30-day learning roadmap for my target role.' },
    { icon: FileText, label: 'Resume Help', preset: 'Review my resume bullets and rewrite them with metrics.' },
    { icon: Target, label: 'Interview Prep', preset: 'Give me a mock interview (DSA + system design + HR).' },
  ]

  const sendMessage = async () => {
    if (!input.trim() || !userId) return

    const userMessage: ChatMessage = { role: 'user', content: input.trim(), timestamp: new Date() }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          message: userMessage.content,
          context: {
            dashboard: dash,
            learning_hours: learningHours,
          },
        }),
      })

      if (!res.ok) throw new Error(`AI route failed: ${res.status}`)
      const data = await res.json()

      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: data?.reply ?? 'Sorry — I could not generate a response.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
    } catch (e) {
      console.error(e)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '⚠️ Model service is not reachable. Check /api/ai/chat and your AI_BACKEND_URL env variable.',
          timestamp: new Date(),
        },
      ])
    } finally {
      setIsTyping(false)
    }
  }

  // ✅ IMPORTANT: No conditional return before hooks.
  // Show loading overlay inside JSX instead.
  const showOverlayLoading = !userId || (loadingStats && !dash)

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {showOverlayLoading && (
        <div className="fixed inset-0 z-50 bg-white/70 backdrop-blur-sm flex items-center justify-center">
          <div className="text-slate-700 font-medium">Loading dashboard…</div>
        </div>
      )}

      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="w-72 bg-white border-r border-slate-200 flex flex-col"
          >
            <div className="p-6 border-b border-slate-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="font-bold text-slate-900">Career AI</h1>
                  <p className="text-xs text-slate-500">Your AI Companion</p>
                </div>
              </div>
            </div>

            <nav className="flex-1 p-4 space-y-1">
              {[
                { icon: Home, label: 'Dashboard', href: '/dashboard' },
                { icon: Briefcase, label: 'Job Matches', href: '/dashboard/jobs' },
                { icon: GraduationCap, label: 'Learning Path', href: '/dashboard/learning' },
                { icon: FileText, label: 'Applications', href: '/dashboard/applications' },
                { icon: Target, label: 'Interview Prep', href: '/dashboard/interview' },
              ].map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all text-slate-600 hover:bg-slate-50"
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                  <ChevronRight className="w-4 h-4 ml-auto opacity-40" />
                </Link>
              ))}
            </nav>

            <div className="p-4 border-t border-slate-200">
              <div className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-50 transition-all">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center text-white font-semibold">
                  {userEmail?.[0]?.toUpperCase() ?? 'U'}
                </div>
                <div className="flex-1">
                  <p className="font-medium text-slate-900">{userEmail ?? 'User'}</p>
                  <p className="text-xs text-slate-500">Logged in</p>
                </div>

                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-600 transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main */}
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <Menu className="w-5 h-5 text-slate-600" />
            </button>
            <div>
              <h2 className="text-xl font-bold text-slate-900">Welcome back! 👋</h2>
              <p className="text-sm text-slate-600">
                {loadingStats ? 'Loading your progress…' : 'Your career dashboard is up to date.'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={loadStats}
              className="px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 transition-colors flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
            <button className="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors flex items-center gap-2">
              <Plus className="w-4 h-4" />
              New Goal
            </button>
          </div>
        </header>

        <div className="p-6">
          <div className="grid grid-cols-4 gap-4 mb-6">
            {stats.map((stat, idx) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.08 }}
                className="bg-white rounded-2xl p-6 border border-slate-200 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 rounded-xl ${stat.bg}`}>
                    <stat.icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                  <Activity className="w-5 h-5 text-slate-300" />
                </div>
                <p className="text-3xl font-bold text-slate-900 mb-1">{stat.value}</p>
                <p className="text-sm text-slate-600">{stat.label}</p>
              </motion.div>
            ))}
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col h-[calc(100vh-340px)]">
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              <AnimatePresence>
                {messages.map((m, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-2xl rounded-2xl px-6 py-4 ${
                        m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-900'
                      }`}
                    >
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{m.content}</p>
                      <p className={`text-xs mt-2 ${m.role === 'user' ? 'text-blue-200' : 'text-slate-500'}`}>
                        {m.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              {isTyping && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                  <div className="bg-slate-100 rounded-2xl px-6 py-4">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200" />
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="px-6 py-3 border-t border-slate-200 bg-slate-50">
              <div className="flex gap-2 overflow-x-auto pb-2">
                {quickActions.map((a) => (
                  <button
                    key={a.label}
                    onClick={() => setInput(a.preset)}
                    className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50 transition-all whitespace-nowrap"
                  >
                    <a.icon className="w-4 h-4 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">{a.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="p-6 border-t border-slate-200">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Ask me anything about your career..."
                  className="flex-1 px-6 py-4 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-slate-900 placeholder:text-slate-400"
                />
                <button
                  onClick={sendMessage}
                  disabled={!input.trim() || !userId}
                  className="px-6 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl hover:shadow-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
              <p className="text-xs text-slate-500 mt-3 text-center">Powered by AI • Your data is secure and private</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
