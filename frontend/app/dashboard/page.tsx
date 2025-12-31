// ============================================
// frontend/app/dashboard/page.tsx
// Main dashboard with chat interface
// ============================================

'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Send, Sparkles, TrendingUp, Briefcase, BookOpen,
  Target, Calendar, Award, ChevronRight, Plus,
  MessageSquare, User, Settings, LogOut, Menu,
  Home, FileText, GraduationCap, BriefcaseIcon
} from 'lucide-react'

export default function Dashboard() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "👋 Hey! I'm your AI career companion. I'm here to help you navigate your career journey. What would you like to work on today?",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [activeTab, setActiveTab] = useState('chat')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const aiMessage = {
        role: 'assistant',
        content: "I understand you're looking for guidance. Let me analyze your profile and find the best opportunities for you. One moment...",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiMessage])
      setIsTyping(false)
    }, 1500)
  }

  const quickActions = [
    { icon: Briefcase, label: 'Find Jobs', action: () => setInput('Show me job opportunities') },
    { icon: BookOpen, label: 'Learning Path', action: () => setInput('Create a learning roadmap') },
    { icon: FileText, label: 'Resume Help', action: () => setInput('Help me improve my resume') },
    { icon: Target, label: 'Interview Prep', action: () => setInput('Practice interview questions') },
  ]

  const stats = [
    { label: 'Skills Tracked', value: '12', icon: Award, color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: 'Jobs Matched', value: '8', icon: Briefcase, color: 'text-green-600', bg: 'bg-green-50' },
    { label: 'Learning Hours', value: '24', icon: BookOpen, color: 'text-purple-600', bg: 'bg-purple-50' },
    { label: 'Applications', value: '5', icon: Target, color: 'text-orange-600', bg: 'bg-orange-50' },
  ]

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="w-72 bg-white border-r border-slate-200 flex flex-col"
          >
            {/* Logo */}
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

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-1">
              {[
                { icon: Home, label: 'Dashboard', id: 'chat' },
                { icon: Briefcase, label: 'Job Matches', id: 'jobs' },
                { icon: GraduationCap, label: 'Learning Path', id: 'learning' },
                { icon: FileText, label: 'Applications', id: 'applications' },
                { icon: Target, label: 'Interview Prep', id: 'interview' },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                    activeTab === item.id
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                  {activeTab === item.id && (
                    <ChevronRight className="w-4 h-4 ml-auto" />
                  )}
                </button>
              ))}
            </nav>

            {/* User Profile */}
            <div className="p-4 border-t border-slate-200">
              <div className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-50 transition-all cursor-pointer">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center text-white font-semibold">
                  JD
                </div>
                <div className="flex-1">
                  <p className="font-medium text-slate-900">John Doe</p>
                  <p className="text-xs text-slate-500">john@example.com</p>
                </div>
                <Settings className="w-5 h-5 text-slate-400" />
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
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
              <p className="text-sm text-slate-600">Let's continue your career journey</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors flex items-center gap-2">
              <Plus className="w-4 h-4" />
              New Goal
            </button>
          </div>
        </header>

        {/* Stats Cards */}
        <div className="p-6">
          <div className="grid grid-cols-4 gap-4 mb-6">
            {stats.map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white rounded-2xl p-6 border border-slate-200 hover:shadow-lg transition-shadow cursor-pointer"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 rounded-xl ${stat.bg}`}>
                    <stat.icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
                <p className="text-3xl font-bold text-slate-900 mb-1">{stat.value}</p>
                <p className="text-sm text-slate-600">{stat.label}</p>
              </motion.div>
            ))}
          </div>

          {/* Chat Interface */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col h-[calc(100vh-340px)]">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              <AnimatePresence>
                {messages.map((message, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-2xl rounded-2xl px-6 py-4 ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-100 text-slate-900'
                      }`}
                    >
                      <p className="text-sm leading-relaxed">{message.content}</p>
                      <p className={`text-xs mt-2 ${
                        message.role === 'user' ? 'text-blue-200' : 'text-slate-500'
                      }`}>
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              {isTyping && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex justify-start"
                >
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

            {/* Quick Actions */}
            <div className="px-6 py-3 border-t border-slate-200 bg-slate-50">
              <div className="flex gap-2 overflow-x-auto pb-2">
                {quickActions.map((action, idx) => (
                  <button
                    key={idx}
                    onClick={action.action}
                    className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50 transition-all whitespace-nowrap"
                  >
                    <action.icon className="w-4 h-4 text-slate-600" />
                    <span className="text-sm font-medium text-slate-700">{action.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Input */}
            <div className="p-6 border-t border-slate-200">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Ask me anything about your career..."
                  className="flex-1 px-6 py-4 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-slate-900 placeholder:text-slate-400"
                />
                <button
                  onClick={sendMessage}
                  disabled={!input.trim()}
                  className="px-6 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl hover:shadow-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
              <p className="text-xs text-slate-500 mt-3 text-center">
                Powered by AI • Your data is secure and private
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}