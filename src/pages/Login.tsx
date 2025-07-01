import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Eye, EyeOff, Check, X, Loader2 } from 'lucide-react';
import { Greeting } from '@/components/Greeting';

export default function Login() {
  const [activeTab, setActiveTab] = useState('login');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [emailValid, setEmailValid] = useState<boolean | null>(null);
  const [rememberMe, setRememberMe] = useState(false);
  
  const [loginData, setLoginData] = useState({
    email: '',
    password: ''
  });
  
  const [registerData, setRegisterData] = useState({
    name: '',
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

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: registerData.name,
          email: registerData.email,
          password: registerData.password
        }),
      });

      if (response.ok) {
        const data = await response.json();
        alert('Conta criada com sucesso! Faça login para continuar.');
        setActiveTab('login');
        setRegisterData({ name: '', email: '', password: '' });
      } else {
        const errorData = await response.json();
        alert(errorData.message || 'Erro no cadastro. Verifique os dados e tente novamente.');
      }
    } catch (error) {
      console.error('Erro no cadastro:', error);
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
            
            {/* VOX text */}
            <div className="text-white font-montserrat font-bold text-4xl tracking-wider mb-2 z-10 relative text-shadow">
              VOX
            </div>
            
            {/* By JT Telecom */}
            <div className="text-white/85 font-opensans text-base z-10 relative tracking-wide">
              by JT Telecom
            </div>
          </div>
          
          <p className="text-2xl mb-4 opacity-90 font-montserrat font-bold text-center">
            Sua comunicação. Mais simples. Mais inteligente.
          </p>
          <p className="text-lg opacity-75 font-opensans text-center">
            Transforme a forma como você se conecta com seus clientes através de tecnologia avançada de comunicação.
          </p>
          <div className="mt-12 space-y-4 w-full">
            <div className="flex items-center justify-center space-x-3">
              <Check className="w-5 h-5 text-jt-green" />
              <span className="font-opensans">Sistema de telefonia integrado</span>
            </div>
            <div className="flex items-center justify-center space-x-3">
              <Check className="w-5 h-5 text-jt-green" />
              <span className="font-opensans">CRM completo e intuitivo</span>
            </div>
            <div className="flex items-center justify-center space-x-3">
              <Check className="w-5 h-5 text-jt-green" />
              <span className="font-opensans">Atendimento automatizado inteligente</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Right Side - Form */}
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-50"
      >
        <div className="w-full max-w-md">
          <Card className="shadow-xl border-0 bg-white">
            <CardHeader className="text-center pb-2">
              <Greeting />
              
              {/* Logo para telas menores - JT Vox */}
              <div className="flex justify-center mb-4 lg:hidden">
                <div className="relative bg-gradient-to-br from-jt-blue to-blue-800 w-64 h-40 rounded-xl flex flex-col items-center justify-center overflow-hidden shadow-xl">
                  {/* Brand container */}
                  <div className="flex items-center gap-3 mb-4 z-10 relative">
                    <div className="bg-white text-jt-blue px-4 py-2 rounded-xl font-montserrat font-black text-lg shadow-md">
                      JT
                    </div>
                    <div className="flex gap-1 items-center">
                      {[14, 22, 18, 26, 12].map((height, index) => (
                        <div
                          key={index}
                          className="w-1 bg-jt-green rounded-full shadow-sm animate-pulse"
                          style={{
                            height: `${height}px`,
                            animationDelay: `${index * 0.2}s`,
                            animationDuration: '1.5s'
                          }}
                        ></div>
                      ))}
                    </div>
                  </div>
                  
                  {/* VOX text */}
                  <div className="text-white font-montserrat font-bold text-2xl tracking-wider mb-1 z-10 relative">
                    VOX
                  </div>
                  
                  {/* By JT Telecom */}
                  <div className="text-white/85 font-opensans text-sm z-10 relative">
                    by JT Telecom
                  </div>
                </div>
              </div>
              
              <CardTitle className="text-2xl font-bold text-jt-blue font-montserrat">
                Bem-vindo
              </CardTitle>
              <CardDescription className="text-jt-gray font-opensans">
                Acesse sua conta ou crie uma nova
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <Tabs 
                value={activeTab} 
                onValueChange={setActiveTab}
                className="w-full"
              >
                <TabsList 
                  className={`grid w-full grid-cols-2 ${
                    isLoading ? 'pointer-events-none opacity-50' : ''
                  }`}
                >
                  <TabsTrigger 
                    value="login"
                    disabled={isLoading}
                    tabIndex={isLoading ? -1 : 0}
                    className="font-opensans"
                  >
                    Entrar
                  </TabsTrigger>
                  <TabsTrigger 
                    value="register"
                    disabled={isLoading}
                    tabIndex={isLoading ? -1 : 0}
                    className="font-opensans"
                  >
                    Cadastrar
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="login">
                  <form onSubmit={handleLogin} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="login-email" className="font-opensans">E-mail</Label>
                      <div className="relative">
                        <Input
                          id="login-email"
                          type="email"
                          placeholder="seu@email.com"
                          value={loginData.email}
                          onChange={handleEmailChange}
                          className={`pr-10 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                          aria-invalid={emailValid === false}
                          aria-describedby={emailValid === false ? "email-error" : undefined}
                          disabled={isLoading}
                          required
                        />
                        {emailValid !== null && (
                          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                            {emailValid ? (
                              <Check 
                                className="h-4 w-4 text-jt-green transition-transform duration-200 hover:scale-110" 
                                aria-label="E-mail válido" 
                              />
                            ) : (
                              <X 
                                className="h-4 w-4 text-red-500 transition-transform duration-200 hover:scale-110" 
                                aria-label="E-mail inválido" 
                              />
                            )}
                          </div>
                        )}
                      </div>
                      {emailValid === false && (
                        <p id="email-error" className="text-sm text-red-500 font-opensans" aria-live="polite">
                          Por favor, insira um e-mail válido
                        </p>
                      )}
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="login-password" className="font-opensans">Senha</Label>
                      <div className="relative">
                        <Input
                          id="login-password"
                          type={showPassword ? 'text' : 'password'}
                          placeholder="Sua senha"
                          value={loginData.password}
                          onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                          className={`pr-10 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                          disabled={isLoading}
                          required
                        />
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                          onClick={() => setShowPassword(!showPassword)}
                          aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
                          disabled={isLoading}
                          tabIndex={isLoading ? -1 : 0}
                        >
                          {showPassword ? (
                            <EyeOff className="h-4 w-4 text-gray-400" />
                          ) : (
                            <Eye className="h-4 w-4 text-gray-400" />
                          )}
                        </Button>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          id="remember"
                          type="checkbox"
                          checked={rememberMe}
                          onChange={(e) => setRememberMe(e.target.checked)}
                          className={`mr-2 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                          disabled={isLoading}
                          tabIndex={isLoading ? -1 : 0}
                        />
                        <label 
                          htmlFor="remember" 
                          className={`text-sm font-opensans ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                          }`}
                        >
                          Manter-me conectado
                        </label>
                      </div>
                      <div>
                        <a 
                          href="/forgot-password" 
                          className={`text-sm text-jt-blue hover:text-blue-800 hover:underline transition-colors focus:outline-none focus:ring-2 focus:ring-blue-300 rounded px-1 font-opensans ${
                            isLoading ? 'pointer-events-none opacity-50' : ''
                          }`}
                          tabIndex={isLoading ? -1 : 0}
                        >
                          Esqueci minha senha?
                        </a>
                      </div>
                    </div>
                    
                    <Button
                      type="submit"
                      className={`w-full bg-jt-blue hover:bg-blue-700 active:bg-blue-800 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                        isLoading ? 'opacity-75 cursor-not-allowed' : ''
                      }`}
                      disabled={isLoading || emailValid === false}
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Entrando...
                        </>
                      ) : (
                        'Entrar'
                      )}
                    </Button>
                    
                    {isLoading && (
                      <div className="mt-4 space-y-2">
                        <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                        <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
                        <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
                      </div>
                    )}
                  </form>
                </TabsContent>
                
                <TabsContent value="register">
                  <form onSubmit={handleRegister} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="register-name" className="font-opensans">Nome completo</Label>
                      <Input
                        id="register-name"
                        placeholder="Seu nome completo"
                        value={registerData.name}
                        onChange={(e) => setRegisterData({ ...registerData, name: e.target.value })}
                        className={`transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                          isLoading ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                        disabled={isLoading}
                        required
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="register-email" className="font-opensans">E-mail</Label>
                      <Input
                        id="register-email"
                        type="email"
                        placeholder="seu@email.com"
                        value={registerData.email}
                        onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })}
                        className={`transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                          isLoading ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                        disabled={isLoading}
                        required
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="register-password" className="font-opensans">Senha</Label>
                      <div className="relative">
                        <Input
                          id="register-password"
                          type={showPassword ? 'text' : 'password'}
                          placeholder="Crie uma senha"
                          value={registerData.password}
                          onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
                          className={`pr-10 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                          disabled={isLoading}
                          required
                        />
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                          onClick={() => setShowPassword(!showPassword)}
                          aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
                          disabled={isLoading}
                          tabIndex={isLoading ? -1 : 0}
                        >
                          {showPassword ? (
                            <EyeOff className="h-4 w-4 text-gray-400" />
                          ) : (
                            <Eye className="h-4 w-4 text-gray-400" />
                          )}
                        </Button>
                      </div>
                    </div>
                    
                    <Button
                      type="submit"
                      className={`w-full bg-jt-blue hover:bg-blue-700 active:bg-blue-800 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-jt-blue font-opensans ${
                        isLoading ? 'opacity-75 cursor-not-allowed' : ''
                      }`}
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Criando conta...
                        </>
                      ) : (
                        'Criar conta'
                      )}
                    </Button>
                    
                    {isLoading && (
                      <div className="mt-4 space-y-2">
                        <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                        <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
                        <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
                      </div>
                    )}
                  </form>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </motion.div>
    </div>
  );
}
