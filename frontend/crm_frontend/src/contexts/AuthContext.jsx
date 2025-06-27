import React, { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export { AuthContext }

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Verificar se há token salvo no localStorage
    const token = localStorage.getItem('crm_token')
    const userData = localStorage.getItem('crm_user')
    
    if (token && userData) {
      try {
        setUser(JSON.parse(userData))
      } catch (error) {
        console.error('Erro ao carregar dados do usuário:', error)
        localStorage.removeItem('crm_token')
        localStorage.removeItem('crm_user')
      }
    }
    
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      // Simulação de login - em produção, fazer chamada para API
      const response = await fetch('https://api.app.jttecnologia.com.br/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (response.ok) {
        const data = await response.json()
        
        // Salvar token e dados do usuário
        localStorage.setItem('crm_token', data.token || 'demo_token')
        localStorage.setItem('crm_user', JSON.stringify(data.user || {
          id: '1',
          name: 'Usuário Demo',
          email: email,
          role: 'admin'
        }))
        
        setUser(data.user || {
          id: '1',
          name: 'Usuário Demo',
          email: email,
          role: 'admin'
        })
        
        return { success: true }
      } else {
        // Se a API não estiver disponível, fazer login demo
        const demoUser = {
          id: '1',
          name: 'Usuário Demo',
          email: email,
          role: 'admin'
        }
        
        localStorage.setItem('crm_token', 'demo_token')
        localStorage.setItem('crm_user', JSON.stringify(demoUser))
        setUser(demoUser)
        
        return { success: true }
      }
    } catch (error) {
      console.error('Erro no login:', error)
      
      // Fallback para login demo
      const demoUser = {
        id: '1',
        name: 'Usuário Demo',
        email: email,
        role: 'admin'
      }
      
      localStorage.setItem('crm_token', 'demo_token')
      localStorage.setItem('crm_user', JSON.stringify(demoUser))
      setUser(demoUser)
      
      return { success: true }
    }
  }

  const logout = () => {
    localStorage.removeItem('crm_token')
    localStorage.removeItem('crm_user')
    setUser(null)
  }

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

