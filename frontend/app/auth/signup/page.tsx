// frontend/app/auth/signup/page.tsx
'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, ArrowLeft, Mail, Lock, User, Eye, EyeOff, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'

const careerGoals = [
  { id: 'first-job', label: 'Land my first job', icon: '🎯' },
  { id: 'switch-career', label: 'Switch careers', icon: '🔄' },
  { id: 'upskill', label: 'Learn new skills', icon: '📚' },
  { id: 'promotion', label: 'Get promoted', icon: '📈' },
  { id: 'freelance', label: 'Start freelancing', icon: '💼' },
  { id: 'entrepreneur', label: 'Build a startup', icon: '🚀' },
]

const experienceLevels = [
  { id: 'student', label: 'Student', description: 'Currently studying' },
  { id: 'entry', label: 'Entry Level', description: '0-2 years experience' },
  { id: 'mid', label: 'Mid Level', description: '3-5 years experience' },
  { id: 'senior', label: 'Senior', description: '5+ years experience' },
]

export default function SignupPage() {
  const router = useRouter()
  
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    careerGoal: '',
    experienceLevel: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  // Email validation
  const validateEmail = (email: string) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
  }

  // Password validation
  const validatePassword = (password: string) => {
    return password.length >= 8
  }

  // Name validation
  const validateName = (name: string) => {
    return name.trim().length >= 2
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // Validation
    if (!validateName(formData.fullName)) {
      setError('Please enter a valid name (at least 2 characters)')
      return
    }

    if (!validateEmail(formData.email)) {
      setError('Please enter a valid email address')
      return
    }

    if (!validatePassword(formData.password)) {
      setError('Password must be at least 8 characters')
      return
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (!formData.careerGoal) {
      setError('Please select a career goal')
      return
    }

    if (!formData.experienceLevel) {
      setError('Please select your experience level')
      return
    }

    setIsLoading(true)

    try {
      // Sign up with Supabase
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: formData.email,
        password: formData.password,
        options: {
          data: {
            full_name: formData.fullName,
            career_goal: formData.careerGoal,
            experience_level: formData.experienceLevel,
          },
          emailRedirectTo: `${window.location.origin}/dashboard`,
        },
      })

      if (authError) throw authError

      if (authData.user) {
        // Create profile in backend
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/profile`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${authData.session?.access_token}`,
            },
            body: JSON.stringify({
              user_id: authData.user.id,
              full_name: formData.fullName,
              career_goal: formData.careerGoal,
              experience_level: formData.experienceLevel,
            }),
          })

          if (!response.ok) {
            console.error('Failed to create profile in backend')
          }
        } catch (profileError) {
          console.error('Profile creation error:', profileError)
          // Continue anyway as auth succeeded
        }

        // Success!
        alert('Account created successfully! Please check your email to verify your account.')
        router.push('/dashboard')
      }
    } catch (err: any) {
      console.error('Signup error:', err)
      setError(err.message || 'Failed to create account. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const nextStep = () => {
    setError('')
    
    if (step === 1) {
      // Validate step 1
      if (!validateName(formData.fullName)) {
        setError('Please enter a valid name')
        return
      }
      if (!validateEmail(formData.email)) {
        setError('Please enter a valid email')
        return
      }
      if (!validatePassword(formData.password)) {
        setError('Password must be at least 8 characters')
        return
      }
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match')
        return
      }
    }
    
    if (step === 2) {
      // Validate step 2
      if (!formData.careerGoal) {
        setError('Please select a career goal')
        return
      }
    }
    
    if (step < 3) setStep(step + 1)
  }

  const prevStep = () => {
    setError('')
    if (step > 1) setStep(step - 1)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Sun */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
        className="absolute top-10 right-10 w-32 h-32 opacity-30"
      >
        <svg viewBox="0 0 100 100" className="w-full h-full">
          <circle cx="50" cy="50" r="20" fill="#FDB022" />
          {[...Array(12)].map((_, i) => (
            <motion.line
              key={i}
              x1="50" y1="10" x2="50" y2="2"
              stroke="#FDB022" strokeWidth="3" strokeLinecap="round"
              transform={`rotate(${i * 30} 50 50)`}
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ duration: 2, repeat: Infinity, delay: i * 0.1 }}
            />
          ))}
        </svg>
      </motion.div>

      {/* Animated Student */}
      <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-10 left-10 w-48 h-48 opacity-20"
      >
        <svg viewBox="0 0 200 200" className="w-full h-full">
          <circle cx="100" cy="60" r="30" fill="#3B82F6" stroke="#1E40AF" strokeWidth="2" />
          <circle cx="90" cy="55" r="3" fill="#1E40AF" />
          <circle cx="110" cy="55" r="3" fill="#1E40AF" />
          <path d="M 85 65 Q 100 75 115 65" fill="none" stroke="#1E40AF" strokeWidth="2" />
          <rect x="80" y="85" width="40" height="50" rx="5" fill="#3B82F6" stroke="#1E40AF" strokeWidth="2" />
          <rect x="120" y="100" width="25" height="18" rx="2" fill="#FDB022" stroke="#D97706" strokeWidth="1.5" />
        </svg>
      </motion.div>

      {/* Floating Sparkles */}
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-yellow-400 rounded-full"
          style={{ left: `${20 + i * 15}%`, top: `${30 + (i % 3) * 20}%` }}
          animate={{ y: [0, -20, 0], opacity: [0.2, 0.8, 0.2], scale: [1, 1.5, 1] }}
          transition={{ duration: 3, repeat: Infinity, delay: i * 0.5 }}
        />
      ))}

      {/* Signup Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-lg bg-white rounded-3xl shadow-2xl p-8 relative z-10"
      >
        {/* Header */}
        <div className="text-center mb-6">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200 }}
            className="inline-block mb-4"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center">
              <span className="text-3xl">🚀</span>
            </div>
          </motion.div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Start Your Journey
          </h1>
          <p className="text-gray-600 text-sm">
            Step {step} of 3: {step === 1 ? 'Account Details' : step === 2 ? 'Career Goals' : 'Experience Level'}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex gap-2">
            {[1, 2, 3].map((s) => (
              <motion.div
                key={s}
                initial={false}
                animate={{ backgroundColor: step >= s ? '#3B82F6' : '#E5E7EB' }}
                className="flex-1 h-2 rounded-full"
              />
            ))}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2"
          >
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-600">{error}</p>
          </motion.div>
        )}

        {/* Form */}
        <AnimatePresence mode="wait">
          {/* Step 1: Account */}
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                    placeholder="John Doe"
                    className="w-full pl-11 pr-4 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all bg-white text-gray-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    placeholder="you@example.com"
                    className="w-full pl-11 pr-4 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all bg-white text-gray-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    placeholder="At least 8 characters"
                    className="w-full pl-11 pr-11 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all bg-white text-gray-900"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                    placeholder="Confirm your password"
                    className="w-full pl-11 pr-11 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all bg-white text-gray-900"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {/* Step 2: Career Goals */}
          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-3"
            >
              <p className="text-sm text-gray-600 mb-4">What's your main career goal?</p>
              <div className="grid grid-cols-2 gap-3">
                {careerGoals.map((goal) => (
                  <motion.button
                    key={goal.id}
                    type="button"
                    onClick={() => setFormData({...formData, careerGoal: goal.id})}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`p-4 rounded-xl border-2 transition-all text-left ${
                      formData.careerGoal === goal.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 bg-white hover:border-blue-200'
                    }`}
                  >
                    <div className="text-2xl mb-2">{goal.icon}</div>
                    <div className="text-sm font-semibold text-gray-900">{goal.label}</div>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Step 3: Experience */}
          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-3"
            >
              <p className="text-sm text-gray-600 mb-4">What's your experience level?</p>
              {experienceLevels.map((level) => (
                <motion.button
                  key={level.id}
                  type="button"
                  onClick={() => setFormData({...formData, experienceLevel: level.id})}
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                  className={`w-full p-4 rounded-xl border-2 transition-all text-left ${
                    formData.experienceLevel === level.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-blue-200'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-gray-900">{level.label}</div>
                      <div className="text-sm text-gray-600">{level.description}</div>
                    </div>
                    {formData.experienceLevel === level.id && (
                      <CheckCircle2 className="w-6 h-6 text-blue-600" />
                    )}
                  </div>
                </motion.button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex gap-3 mt-6">
          {step > 1 && (
            <button
              type="button"
              onClick={prevStep}
              className="px-6 py-3 rounded-xl border-2 border-gray-200 text-gray-700 font-semibold hover:bg-gray-50 transition-all flex items-center gap-2"
            >
              <ArrowLeft className="w-5 h-5" />
              Back
            </button>
          )}
          {step < 3 ? (
            <button
              type="button"
              onClick={nextStep}
              className="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold py-3 rounded-xl hover:shadow-lg transition-all flex items-center justify-center gap-2"
            >
              Continue
              <ArrowRight className="w-5 h-5" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={isLoading}
              className="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold py-3 rounded-xl hover:shadow-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  Create Account
                  <Sparkles className="w-5 h-5" />
                </>
              )}
            </button>
          )}
        </div>

        {/* Login Link */}
        <p className="text-center mt-6 text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/" className="font-semibold text-blue-600 hover:text-blue-700">
            Sign in
          </Link>
        </p>
      </motion.div>
    </div>
  )
}