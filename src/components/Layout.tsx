
import React from 'react';
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import NotificationSystemAdvanced from "@/components/NotificationSystemAdvanced";
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { LogOut, User } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-gray-50">
        <AppSidebar />
        
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="h-16 bg-jt-white shadow-sm border-b flex items-center justify-between px-6">
            <div className="flex items-center gap-4">
              <SidebarTrigger className="text-jt-blue" />
              
              {/* JT Vox Logo Compacto */}
              <div className="flex items-center gap-2">
                <div className="bg-jt-blue text-white px-2 py-1 rounded-lg font-montserrat font-black text-sm shadow-sm">
                  JT
                </div>
                <div className="flex gap-0.5 items-center">
                  {[8, 12, 10, 14, 7].map((height, index) => (
                    <div
                      key={index}
                      className="w-0.5 bg-jt-green rounded-full animate-pulse"
                      style={{
                        height: `${height}px`,
                        animationDelay: `${index * 0.2}s`,
                        animationDuration: '1.5s'
                      }}
                    ></div>
                  ))}
                </div>
                <span className="text-jt-blue font-montserrat font-bold text-lg tracking-wide">
                  VOX
                </span>
              </div>
            </div>
            
            {/* Sistema de Notificações Avançado */}
            <div className="flex-1 flex justify-center">
              <NotificationSystemAdvanced userId={user?.id} />
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{user?.name}</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={logout}
                className="flex items-center gap-2 border-jt-blue text-jt-blue hover:bg-jt-blue hover:text-jt-white"
              >
                <LogOut className="w-4 h-4" />
                Sair
              </Button>
            </div>
          </header>
          
          {/* Main Content */}
          <main className="flex-1 p-6">
            {children}
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Layout;
