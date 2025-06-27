import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
    remember: false
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Credenciais demo
      if (credentials.username === 'admin' && credentials.password === 'admin') {
        const result = await login('admin@jttecnologia.com.br', 'admin');
        if (!result.success) {
          setError('Erro ao fazer login. Tente novamente.');
        }
      } else {
        setError('Usuário ou senha incorretos. Tente novamente.');
      }
    } catch (err) {
      setError('Erro ao fazer login. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 flex items-center justify-center overflow-hidden relative">
      {/* Animação de fundo com formas flutuantes */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-20 h-20 bg-white bg-opacity-10 rounded-full top-1/5 left-1/10 animate-float"></div>
        <div className="absolute w-30 h-30 bg-white bg-opacity-10 rounded-full top-3/5 right-1/6 animate-float-delayed-2"></div>
        <div className="absolute w-15 h-15 bg-white bg-opacity-10 rounded-full bottom-1/5 left-1/5 animate-float-delayed-4"></div>
        <div className="absolute w-25 h-25 bg-white bg-opacity-10 rounded-full top-1/10 right-1/4 animate-float-delayed-6"></div>
      </div>

      {/* Container principal */}
      <div className="flex bg-white bg-opacity-95 rounded-3xl shadow-2xl overflow-hidden max-w-4xl w-full min-h-[500px] relative z-10 backdrop-blur-sm mx-4">
        
        {/* Lado esquerdo - Ilustração */}
        <div className="flex-1 bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 flex flex-col items-center justify-center text-white relative p-10 text-center">
          
          {/* Logo */}
          <div className="absolute top-8 left-8 flex items-center gap-3">
            <div className="w-15 h-15 bg-white rounded-xl flex items-center justify-center shadow-lg p-2">
              <img 
                src="https://crm.jttecnologia.com.br/media/JT-Telecom-LOGO1.jpg?_t=1727781649" 
                alt="JT Telecom Logo"
                className="w-full h-full object-contain rounded-lg"
              />
            </div>
            <div className="text-lg font-bold text-white drop-shadow-sm">
              JT Telecom
            </div>
          </div>

          {/* Ilustração central */}
          <div className="mb-8">
            <div className="w-30 h-30 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-5 animate-pulse relative">
              <div className="absolute w-35 h-35 border-2 border-white border-opacity-30 rounded-full animate-ping"></div>
              <i className="fas fa-phone text-4xl text-white"></i>
            </div>
            <div>
              <h2 className="text-3xl mb-2 font-bold">Bem-vindo de volta!</h2>
              <p className="text-base opacity-90 leading-relaxed">
                Acesse seu CRM e gerencie seus leads, vendas e oportunidades de forma inteligente.
              </p>
            </div>
          </div>
        </div>

        {/* Lado direito - Formulário */}
        <div className="flex-1 p-12 flex flex-col justify-center">
          <div className="text-center mb-10">
            <h1 className="text-3xl text-gray-800 mb-2 font-bold">Fazer Login</h1>
            <p className="text-gray-600 text-base">Entre com suas credenciais para acessar o sistema</p>
          </div>

          {/* Mensagem de erro */}
          {error && (
            <div className="bg-red-100 text-red-700 p-3 rounded-lg text-sm mb-4 border border-red-200 animate-slideDown">
              <i className="fas fa-exclamation-triangle mr-2"></i>
              {error}
            </div>
          )}

          {/* Formulário de login */}
          <form onSubmit={handleSubmit} className="flex flex-col gap-6">
            <div>
              <label htmlFor="username" className="block mb-2 text-gray-700 font-medium text-sm">
                Usuário
              </label>
              <div className="relative">
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={credentials.username}
                  onChange={handleChange}
                  className="w-full p-4 pl-12 border-2 border-gray-200 rounded-xl text-base transition-all duration-300 bg-gray-50 focus:outline-none focus:border-blue-500 focus:bg-white focus:shadow-lg"
                  placeholder="Digite seu usuário"
                  required
                />
                <i className="fas fa-user absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block mb-2 text-gray-700 font-medium text-sm">
                Senha
              </label>
              <div className="relative">
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={credentials.password}
                  onChange={handleChange}
                  className="w-full p-4 pl-12 border-2 border-gray-200 rounded-xl text-base transition-all duration-300 bg-gray-50 focus:outline-none focus:border-blue-500 focus:bg-white focus:shadow-lg"
                  placeholder="Digite sua senha"
                  required
                />
                <i className="fas fa-lock absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
              </div>
            </div>

            <div className="flex justify-between items-center my-2">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="remember"
                  name="remember"
                  checked={credentials.remember}
                  onChange={handleChange}
                  className="w-4 h-4 accent-blue-600"
                />
                <label htmlFor="remember" className="text-gray-700 text-sm">
                  Lembrar de mim
                </label>
              </div>
              <a href="#" className="text-blue-600 text-sm font-medium hover:text-blue-800 transition-colors">
                Esqueceu a senha?
              </a>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`bg-gradient-to-r from-blue-600 to-purple-600 text-white border-none p-4 rounded-xl text-base font-semibold cursor-pointer transition-all duration-300 relative overflow-hidden ${
                loading ? 'pointer-events-none' : 'hover:-translate-y-0.5 hover:shadow-xl'
              }`}
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-transparent border-t-white rounded-full animate-spin mr-2"></div>
                  Entrando...
                </div>
              ) : (
                'Entrar'
              )}
            </button>
          </form>

          {/* Credenciais demo */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-sm text-blue-800 font-medium mb-2">
              <i className="fas fa-info-circle mr-2"></i>
              Credenciais de demonstração:
            </p>
            <p className="text-sm text-blue-700">
              <strong>Usuário:</strong> admin<br />
              <strong>Senha:</strong> admin
            </p>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0px) rotate(0deg);
            opacity: 0.3;
          }
          25% {
            transform: translateY(-20px) rotate(90deg);
            opacity: 0.6;
          }
          50% {
            transform: translateY(-40px) rotate(180deg);
            opacity: 0.4;
          }
          75% {
            transform: translateY(-20px) rotate(270deg);
            opacity: 0.7;
          }
        }

        .animate-float {
          animation: float 15s infinite ease-in-out;
        }

        .animate-float-delayed-2 {
          animation: float 15s infinite ease-in-out;
          animation-delay: 2s;
        }

        .animate-float-delayed-4 {
          animation: float 15s infinite ease-in-out;
          animation-delay: 4s;
        }

        .animate-float-delayed-6 {
          animation: float 15s infinite ease-in-out;
          animation-delay: 6s;
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-slideDown {
          animation: slideDown 0.3s ease;
        }

        @media (max-width: 768px) {
          .flex {
            flex-direction: column;
          }
          
          .flex-1:first-child {
            padding: 30px;
            min-height: 250px;
          }
          
          .absolute.top-8.left-8 {
            position: static;
            margin-bottom: 20px;
            justify-content: center;
          }
        }
      `}</style>
    </div>
  );
};

export default Login;

