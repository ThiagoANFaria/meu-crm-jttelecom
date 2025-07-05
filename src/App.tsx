import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";
import ProtectedRoute from "@/components/ProtectedRoute";
import Layout from "@/components/Layout";
import Login from "@/pages/LoginNew";
import Dashboard from "@/pages/DashboardSimple";
import DashboardAnalytics from "@/pages/DashboardAnalytics";
import DashboardAnalyticsAdvanced from "@/pages/DashboardAnalyticsAdvanced";
import AdvancedReportsEnhanced from "@/pages/AdvancedReportsEnhanced";
import Configuration from "@/pages/Configuration";
import Proposals from "@/pages/Proposals";
import MasterPanel from "@/pages/MasterPanelSimple";
import TenantAdminPanel from "@/pages/TenantAdminPanel";
import Clients from "@/pages/Clients";
import ClientDetail from "@/pages/ClientDetail";
import Leads from "@/pages/Leads";
import LeadDetail from "@/pages/LeadDetail";
import Contracts from "@/pages/Contracts";
import Tasks from "@/pages/Tasks";
import Pipelines from "@/pages/Pipelines";
import Telephony from "@/pages/Telephony";
import Chatbot from "@/pages/Chatbot";
import Automation from "@/pages/Automation";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <AuthProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Navigate to="/login" replace />} />
            
            {/* Rota Master - Admin Master JT Telecom */}
            <Route path="/master" element={
              <ProtectedRoute requiredLevel="master">
                <MasterPanel />
              </ProtectedRoute>
            } />
            
            {/* Rota Admin - Admin da Tenant */}
            <Route path="/admin" element={
              <ProtectedRoute requiredLevel="admin">
                <TenantAdminPanel />
              </ProtectedRoute>
            } />
            
            {/* Rota Admin Dashboard - Admin da Tenant com acesso ao CRM */}
            <Route path="/admin/dashboard" element={
              <ProtectedRoute requiredLevel="admin">
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            } />
            
            {/* Rotas do CRM - Usuários finais */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/clients" element={
              <ProtectedRoute>
                <Layout>
                  <Clients />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/clients/:id" element={
              <ProtectedRoute>
                <Layout>
                  <ClientDetail />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/leads" element={
              <ProtectedRoute>
                <Layout>
                  <Leads />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/leads/:id" element={
              <ProtectedRoute>
                <Layout>
                  <LeadDetail />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/contracts" element={
              <ProtectedRoute>
                <Layout>
                  <Contracts />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/proposals" element={
              <ProtectedRoute>
                <Layout>
                  <Proposals />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/tasks" element={
              <ProtectedRoute>
                <Layout>
                  <Tasks />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/pipelines" element={
              <ProtectedRoute>
                <Layout>
                  <Pipelines />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/telephony" element={
              <ProtectedRoute>
                <Layout>
                  <Telephony />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/chatbot" element={
              <ProtectedRoute>
                <Layout>
                  <Chatbot />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/automation" element={
              <ProtectedRoute>
                <Layout>
                  <Automation />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/analytics" element={
              <ProtectedRoute>
                <Layout>
                  <DashboardAnalyticsAdvanced />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/reports" element={
              <ProtectedRoute>
                <Layout>
                  <AdvancedReportsEnhanced />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/configuration" element={
              <ProtectedRoute requiredLevel="admin">
                <Layout>
                  <Configuration />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </AuthProvider>
  </QueryClientProvider>
);

export default App;

