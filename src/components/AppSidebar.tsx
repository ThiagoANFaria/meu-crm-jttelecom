import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar';
import {
  LayoutDashboard,
  Users,
  UserPlus,
  FileText,
  FileCheck,
  CheckSquare,
  GitBranch,
  MessageCircle,
  Phone,
  Zap,
} from 'lucide-react';

const menuItems = [
  {
    title: 'Dashboard',
    url: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    title: 'Leads',
    url: '/leads',
    icon: UserPlus,
  },
  {
    title: 'Clientes',
    url: '/clients',
    icon: Users,
  },
  {
    title: 'Propostas',
    url: '/proposals',
    icon: FileText,
  },
  {
    title: 'Contratos',
    url: '/contracts',
    icon: FileCheck,
  },
  {
    title: 'Tarefas',
    url: '/tasks',
    icon: CheckSquare,
  },
  {
    title: 'Pipelines',
    url: '/pipelines',
    icon: GitBranch,
  },
  {
    title: 'Chatbot',
    url: '/chatbot',
    icon: MessageCircle,
  },
  {
    title: 'Telefonia',
    url: '/telephony',
    icon: Phone,
  },
  {
    title: 'Automação',
    url: '/automation',
    icon: Zap,
  },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const location = useLocation();
  const isCollapsed = state === 'collapsed';

  return (
    <Sidebar className="border-r border-gray-200 bg-jt-white">
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-jt-blue font-semibold">
            JT Vox
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => {
                const isActive = location.pathname === item.url;
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild>
                      <NavLink
                        to={item.url}
                        className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                          isActive
                            ? 'bg-jt-blue text-jt-white'
                            : 'text-gray-600 hover:bg-blue-50 hover:text-jt-blue'
                        }`}
                      >
                        <item.icon className="w-5 h-5" />
                        {!isCollapsed && <span>{item.title}</span>}
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}

