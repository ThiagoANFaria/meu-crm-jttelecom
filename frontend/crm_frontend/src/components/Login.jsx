import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Eye, EyeOff, Mail, Lock, CheckCircle } from 'lucide-react'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const { login } = useAuth()

  const handleSubmit = (e) => {
    e.preventDefault()
    login(email, password)
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Left Side - Login Form */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-20 xl:px-24">
        <div className="max-w-md w-full space-y-8">
          {/* Logo */}
          <div className="text-center">
            <img
              src="https://crm.jttecnologia.com.br/media/JT-Telecom-LOGO1.jpg?_t=1727781649"
              alt="JT Telecom"
              className="h-16 w-auto mx-auto mb-8"
            />
          </div>

          {/* Welcome Text */}
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Olá, Bem-vindo de volta!
            </h2>
            <p className="text-gray-600 text-sm">
              Faça login para acessar sua conta JT Telecom
            </p>
          </div>

          {/* Login Form */}
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-4">
              {/* Email Field */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    placeholder="seu@email.com"
                  />
                </div>
              </div>

              {/* Password Field */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Senha
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="block w-full pl-10 pr-12 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <button
                  type="button"
                  onClick={() => setRememberMe(!rememberMe)}
                  className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
                    rememberMe 
                      ? 'bg-blue-600 border-blue-600' 
                      : 'border-gray-300 hover:border-blue-500'
                  }`}>
                    {rememberMe && <CheckCircle className="w-3 h-3 text-white" />}
                  </div>
                  <span>Lembrar de mim</span>
                </button>
              </div>
              <a href="#" className="text-sm text-blue-600 hover:text-blue-500 font-medium">
                Esqueceu a senha?
              </a>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-[1.02]"
            >
              Entrar no CRM
            </button>

            {/* Demo Credentials */}
            <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
              <p className="text-xs text-blue-800 font-medium mb-2">Credenciais de Demonstração:</p>
              <p className="text-xs text-blue-700">
                <strong>Email:</strong> admin@jttelecom.com<br />
                <strong>Senha:</strong> qualquer senha
              </p>
            </div>
          </form>

          {/* Footer */}
          <div className="text-center">
            <p className="text-xs text-gray-500">
              © 2024 JT Telecom. Todos os direitos reservados.
            </p>
          </div>
        </div>
      </div>

      {/* Right Side - Illustration */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-32 h-32 bg-white rounded-full"></div>
          <div className="absolute top-40 right-32 w-24 h-24 bg-white rounded-full"></div>
          <div className="absolute bottom-32 left-32 w-40 h-40 bg-white rounded-full"></div>
          <div className="absolute bottom-20 right-20 w-28 h-28 bg-white rounded-full"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center items-center text-center px-12">
          <div className="max-w-md">
            {/* Icon/Illustration */}
            <div className="mb-8">
              <div className="w-32 h-32 mx-auto bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center">
                  <Lock className="w-10 h-10 text-blue-600" />
                </div>
              </div>
            </div>

            {/* Text */}
            <h3 className="text-3xl font-bold text-white mb-4">
              Sistema Seguro
            </h3>
            <p className="text-blue-100 text-lg leading-relaxed">
              Acesse seu CRM com total segurança. Seus dados estão protegidos com a mais alta tecnologia de criptografia.
            </p>

            {/* Features */}
            <div className="mt-8 space-y-3">
              <div className="flex items-center text-blue-100">
                <CheckCircle className="w-5 h-5 mr-3 text-green-300" />
                <span>Autenticação segura</span>
              </div>
              <div className="flex items-center text-blue-100">
                <CheckCircle className="w-5 h-5 mr-3 text-green-300" />
                <span>Dados criptografados</span>
              </div>
              <div className="flex items-center text-blue-100">
                <CheckCircle className="w-5 h-5 mr-3 text-green-300" />
                <span>Acesso 24/7</span>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-white opacity-5 rounded-full -translate-y-32 translate-x-32"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-tr from-white opacity-5 rounded-full translate-y-48 -translate-x-48"></div>
      </div>
    </div>
  )
}

export default Login

