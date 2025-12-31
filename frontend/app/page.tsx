'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react'
import Link from 'next/link'  // Add this at the top with other imports
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'

const handleGoogleLogin = async () => {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/dashboard`,
    },
  })

  if (error) alert(error.message)
}

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  
  const handleLogin = async () => {
  if (!email || !password) {
    window.alert('Enter email and password')
    return
  }

  setIsLoading(true)

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  setIsLoading(false)

  if (error) {
    window.alert(error.message)
    return
  }

  router.push('/dashboard')
}

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Sun */}
      <motion.div
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: 60,
          repeat: Infinity,
          ease: "linear"
        }}
        className="absolute top-10 right-10 w-32 h-32 opacity-30"
      >
        <svg viewBox="0 0 100 100" className="w-full h-full">
          <circle cx="50" cy="50" r="20" fill="#FDB022" />
          {[...Array(12)].map((_, i) => (
            <motion.line
              key={i}
              x1="50"
              y1="10"
              x2="50"
              y2="2"
              stroke="#FDB022"
              strokeWidth="3"
              strokeLinecap="round"
              transform={`rotate(${i * 30} 50 50)`}
              animate={{
                opacity: [0.3, 1, 0.3],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.1,
              }}
            />
          ))}
        </svg>
      </motion.div>

      {/* Animated Student Character */}
      <motion.div
        animate={{
          y: [0, -10, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="absolute bottom-10 left-10 w-48 h-48 opacity-20"
      >
        <svg viewBox="0 0 200 200" className="w-full h-full">
          {/* Head */}
          <circle cx="100" cy="60" r="30" fill="#3B82F6" stroke="#1E40AF" strokeWidth="2" />
          
          {/* Happy Face */}
          <circle cx="90" cy="55" r="3" fill="#1E40AF" />
          <circle cx="110" cy="55" r="3" fill="#1E40AF" />
          <motion.path
            d="M 85 65 Q 100 75 115 65"
            fill="none"
            stroke="#1E40AF"
            strokeWidth="2"
            strokeLinecap="round"
            animate={{
              d: [
                "M 85 65 Q 100 75 115 65",
                "M 85 65 Q 100 78 115 65",
                "M 85 65 Q 100 75 115 65",
              ]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
            }}
          />
          
          {/* Body */}
          <rect x="80" y="85" width="40" height="50" rx="5" fill="#3B82F6" stroke="#1E40AF" strokeWidth="2" />
          
          {/* Arms */}
          <motion.line
            x1="80"
            y1="95"
            x2="60"
            y2="105"
            stroke="#3B82F6"
            strokeWidth="6"
            strokeLinecap="round"
            animate={{
              x2: [60, 55, 60],
              y2: [105, 100, 105],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
            }}
          />
          <motion.line
            x1="120"
            y1="95"
            x2="140"
            y2="105"
            stroke="#3B82F6"
            strokeWidth="6"
            strokeLinecap="round"
            animate={{
              x2: [140, 145, 140],
              y2: [105, 100, 105],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: 0.5,
            }}
          />
          
          {/* Legs */}
          <rect x="85" y="135" width="12" height="30" rx="3" fill="#3B82F6" stroke="#1E40AF" strokeWidth="2" />
          <rect x="103" y="135" width="12" height="30" rx="3" fill="#3B82F6" stroke="#1E40AF" strokeWidth="2" />
          
          {/* Book */}
          <motion.rect
            x="120"
            y="100"
            width="25"
            height="18"
            rx="2"
            fill="#FDB022"
            stroke="#D97706"
            strokeWidth="1.5"
            animate={{
              rotate: [0, -5, 0],
              x: [120, 122, 120],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
            }}
            style={{ transformOrigin: "120px 109px" }}
          />
          <line x1="132.5" y1="100" x2="132.5" y2="118" stroke="#D97706" strokeWidth="1" />
        </svg>
      </motion.div>

      {/* Floating Sparkles */}
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-yellow-400 rounded-full"
          style={{
            left: `${20 + i * 15}%`,
            top: `${30 + (i % 3) * 20}%`,
          }}
          animate={{
            y: [0, -20, 0],
            opacity: [0.2, 0.8, 0.2],
            scale: [1, 1.5, 1],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            delay: i * 0.5,
          }}
        />
      ))}

      {/* Login Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 relative z-10"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-block mb-4"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center">
              <span className="text-3xl">🎓</span>
            </div>
          </motion.div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome Back!
          </h1>
          <p className="text-gray-600 text-sm">
            Continue your learning journey
          </p>
        </div>

        {/* Form Fields */}
        <div className="space-y-5">
          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full pl-11 pr-4 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all bg-white text-gray-900"
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
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

          {/* Forgot Password */}
          <div className="text-right">
            <button type="button" className="text-sm text-blue-600 hover:text-blue-700">
              Forgot password?
            </button>
          </div>

          {/* Submit Button */}
          <motion.button
            type="button"
            onClick={handleLogin}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold py-3 rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Signing in...
              </>
            ) : (
              <>
                Sign in
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </motion.button>
        </div>

        {/* Divider */}
        <div className="my-6 text-center">
          <span className="text-sm text-gray-500">or</span>
        </div>

        {/* Social Login */}
        <div className="space-y-3">
          <button
  type="button"
  onClick={handleGoogleLogin}
  className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-xl border border-gray-200 bg-white hover:bg-gray-50 transition-colors">
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
              <span className="font-medium text-gray-700">Continue with Google</span>
          </button>
        </div>

        {/* Sign Up Link */}
        {/* Sign Up Link */}
      <p className="text-center mt-6 text-sm text-gray-600">
        Don't have an account?{' '}
        <Link href="/auth/signup" className="font-semibold text-blue-600 hover:text-blue-700">
          Sign up free
        </Link>
      </p>
      </motion.div>
    </div>
  )
}