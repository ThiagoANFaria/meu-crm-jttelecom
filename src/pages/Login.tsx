import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Eye, EyeOff, Check, X, Loader2, Building2 } from 'lucide-react';
import { Greeting } from '@/components/Greeting';

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [emailValid, setEmailValid] = useState<boolean | null>(null);
  const [rememberMe, setRememberMe] = useState(false);
  
  const [loginData, setLoginData] = useState({
    email: '',
    password: ''
  });

  // Validação de e-mail em tempo real
  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const email = e.target.value;
    setLoginData({ ...loginData, email });
    
    if (email.length > 0) {
      setEmailValid(validateEmail(email));
    } else {
      setEmailValid(null);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: loginData.email,
          password: loginData.password
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        if (rememberMe) {
          localStorage.setItem('rememberMe', 'true');
        }
        // Redirecionar para dashboard
        window.location.href = '/dashboard';
      } else {
        const errorData = await response.json();
        alert(errorData.message || 'Erro no login. Verifique suas credenciais.');
      }
    } catch (error) {
      console.error('Erro no login:', error);
      alert('Erro de conexão. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding */}
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-jt-blue to-blue-800 flex-col justify-center items-center p-12 text-white"
      >
        <div className="max-w-md text-center flex flex-col items-center">
          {/* JT Vox Logo */}
          <div className="relative bg-gradient-to-br from-jt-blue to-blue-800 w-80 h-52 rounded-xl flex flex-col items-center justify-center mb-8 overflow-hidden shadow-2xl">
            {/* Animated background effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse"></div>
            
            {/* Brand container */}
            <div className="flex items-center gap-4 mb-6 z-10 relative">
              <div className="bg-white text-jt-blue px-5 py-3 rounded-2xl font-montserrat font-black text-2xl shadow-lg">
                JT
              </div>
              <div className="flex gap-1 items-center">
                {[18, 28, 22, 34, 16].map((height, index) => (
                  <div
                    key={index}
                    className="w-1.5 bg-jt-green rounded-full shadow-lg animate-pulse"
                    style={{
                      height: `${height}px`,
                      animationDelay: `${index * 0.2}s`,
                      animationDuration: '1.5s'
                    }}
                  ></div>
                ))}
              </div>
            </div>
            
            {/* VOX Title */}
            <h1 className="text-4xl font-bold mb-2 z-10 relative">VOX</h1>
            <p className="text-blue-200 text-sm z-10 relative">by JT Telecom</p>
          </div>
          
          {/* Marketing content */}
          <h2 className="text-3xl font-bold mb-6">
            Sua comunicação. Mais simples.<br />
            Mais inteligente.
          </h2>
          
          <p className="text-blue-100 mb-8 leading-relaxed">
            Transforme a forma como você se conecta com seus clientes através de tecnologia avançada de comunicação.
          </p>
          
          {/* Features */}
          <div className="space-y-4 text-left">
            <div className="flex items-center gap-3">
              <Check className="w-5 h-5 text-jt-green" />
              <span>Sistema de telefonia integrado</span>
            </div>
            <div className="flex items-center gap-3">
              <Check className="w-5 h-5 text-jt-green" />
              <span>CRM completo e intuitivo</span>
            </div>
            <div className="flex items-center gap-3">
              <Check className="w-5 h-5 text-jt-green" />
              <span>Atendimento automatizado inteligente</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Right Side - Login Form */}
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="flex-1 flex items-center justify-center p-8 bg-gray-50"
      >
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <Greeting />
          </div>

          <Card className="shadow-xl border-0">
            <CardHeader className="text-center pb-4">
              <CardTitle className="text-2xl font-bold text-gray-900">Bem-vindo</CardTitle>
              <CardDescription className="text-gray-600">
                Acesse sua conta empresarial
              </CardDescription>
              
              {/* Multi-tenant indicator */}
              <div className="flex items-center justify-center gap-2 mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <Building2 className="w-4 h-4 text-blue-600" />
                <span className="text-sm text-blue-700 font-medium">Sistema Empresarial Multi-tenant</span>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-6">
              <form onSubmit={handleLogin} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">E-mail</Label>
                  <div className="relative">
                    <Input
                      id="email"
                      type="email"
                      placeholder="seu@email.com"
                      value={loginData.email}
                      onChange={handleEmailChange}
                      className={`pr-10 ${
                        emailValid === true ? 'border-green-500' : 
                        emailValid === false ? 'border-red-500' : ''
                      }`}
                      required
                    />
                    {emailValid !== null && (
                      <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                        {emailValid ? (
                          <Check className="w-4 h-4 text-green-500" />
                        ) : (
                          <X className="w-4 h-4 text-red-500" />
                        )}
                      </div>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Senha</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Sua senha"
                      value={loginData.password}
                      onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                      className="pr-10"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="remember"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="rounded border-gray-300"
                    />
                    <Label htmlFor="remember" className="text-sm text-gray-600">
                      Manter-me conectado
                    </Label>
                  </div>
                  <a href="#" className="text-sm text-jt-blue hover:underline">
                    Esqueci minha senha?
                  </a>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-jt-blue hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Entrando...
                    </>
                  ) : (
                    'Entrar'
                  )}
                </Button>
              </form>

              {/* Multi-tenant info */}
              <div className="mt-6 p-4 bg-gray-50 rounded-lg border">
                <h4 className="font-semibold text-gray-900 mb-2">Precisa de acesso?</h4>
                <p className="text-sm text-gray-600 mb-3">
                  Este é um sistema empresarial. Para obter acesso, entre em contato com o administrador da sua empresa.
                </p>
                <div className="text-xs text-gray-500">
                  <strong>Suporte:</strong> admin@jttecnologia.com.br
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </motion.div>
    </div>
  );
}

