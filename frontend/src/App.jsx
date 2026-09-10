import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AccessibilityProvider } from './context/AccessibilityContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { ScanStudioPage } from './pages/ScanStudioPage';
import { InspectionDetailPage } from './pages/InspectionDetailPage';
import { InspectionHistoryPage } from './pages/InspectionHistoryPage';
import { ProductRepositoryPage } from './pages/ProductRepositoryPage';
import { RuleLibraryPage } from './pages/RuleLibraryPage';
import { AuditTrailPage } from './pages/AuditTrailPage';
import { LoginPage } from './pages/LoginPage';

function MainApp() {
  const { user } = useAuth();
  const [currentTab, setCurrentTab] = useState('landing');
  const [selectedInspectionId, setSelectedInspectionId] = useState(null);

  const handleNavigate = (tab) => {
    setCurrentTab(tab);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectInspection = (id) => {
    setSelectedInspectionId(id);
    setCurrentTab('inspection-detail');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleScanComplete = (newInspectionId) => {
    setSelectedInspectionId(newInspectionId);
    setCurrentTab('inspection-detail');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col font-sans w-full overflow-x-hidden">
      <Navbar onNavigate={handleNavigate} currentTab={currentTab} />

      <div className="flex-1 flex w-full min-w-0">
        {/* Render sidebar on non-landing, non-login pages */}
        {currentTab !== 'landing' && currentTab !== 'login' && (
          <Sidebar currentTab={currentTab} onNavigate={handleNavigate} />
        )}

        <main className={`flex-1 min-w-0 ${currentTab === 'landing' ? 'w-full' : 'p-4 sm:p-6 lg:p-8 max-w-[1550px]'}`}>
          {currentTab === 'landing' && (
            <LandingPage onNavigate={handleNavigate} />
          )}

          {currentTab === 'dashboard' && (
            <DashboardPage 
              onNavigate={handleNavigate} 
              onSelectInspection={handleSelectInspection} 
            />
          )}

          {currentTab === 'scan' && (
            <ScanStudioPage 
              onScanComplete={handleScanComplete}
            />
          )}

          {currentTab === 'inspection-detail' && (
            <InspectionDetailPage 
              inspectionId={selectedInspectionId || 'PRM-20260830-COMP01'} 
              onBack={() => handleNavigate('inspections')} 
            />
          )}

          {currentTab === 'inspections' && (
            <InspectionHistoryPage 
              onSelectInspection={handleSelectInspection} 
            />
          )}

          {currentTab === 'products' && (
            <ProductRepositoryPage 
              onSelectInspection={handleSelectInspection} 
            />
          )}

          {currentTab === 'rules' && (
            <RuleLibraryPage />
          )}

          {currentTab === 'audit' && (
            <AuditTrailPage />
          )}

          {currentTab === 'login' && (
            <LoginPage onLoginSuccess={() => handleNavigate('dashboard')} />
          )}
        </main>
      </div>

      {/* Official Compact Regulatory Footer */}
      <footer className="bg-[#0B1B33] text-slate-300 text-xs border-t border-slate-800/90 py-3.5 px-4 sm:px-8">
        <div className="max-w-[1550px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
          <div className="flex flex-wrap items-center gap-2 justify-center sm:justify-start">
            <span className="font-bold text-white tracking-tight font-heading">PRAMAN AI</span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-300">Packaging Regulations & Automated Metrology Audit Network</span>
            <span className="text-slate-500 hidden md:inline">•</span>
            <span className="text-slate-400 text-[11px] hidden md:inline">SIH 2026 • Legal Metrology Act 2009 & PCR 2011</span>
          </div>
          <div className="flex items-center gap-4 text-xs">
            <button onClick={() => handleNavigate('rules')} className="text-slate-300 hover:text-white transition-colors underline-offset-4 hover:underline">
              Rule Knowledge Base (40 PDFs)
            </button>
            <span className="text-slate-600">•</span>
            <button onClick={() => handleNavigate('audit')} className="text-slate-300 hover:text-white transition-colors underline-offset-4 hover:underline">
              Audit Logs
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AccessibilityProvider>
        <MainApp />
      </AccessibilityProvider>
    </AuthProvider>
  );
}
