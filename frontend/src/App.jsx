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
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col font-sans">
      <Navbar onNavigate={handleNavigate} currentTab={currentTab} />

      <div className="flex-1 flex max-w-[1600px] w-full mx-auto">
        {/* Render sidebar on non-landing pages or when requested */}
        {currentTab !== 'landing' && currentTab !== 'login' && (
          <Sidebar currentTab={currentTab} onNavigate={handleNavigate} />
        )}

        <main className={`flex-1 p-4 sm:p-6 lg:p-8 ${currentTab === 'landing' ? 'max-w-7xl mx-auto w-full' : ''}`}>
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

      {/* Official Government of India & SIH 2026 Footer */}
      <footer className="bg-[#0B192C] text-slate-400 text-xs border-t border-slate-800 py-6 px-4">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
          <div>
            <span className="font-bold text-slate-200 font-['Outfit']">PRAMAN AI</span>
            <span className="text-slate-500 mx-2">•</span>
            <span>Packaging Regulations & Automated Metrology Audit Network</span>
            <p className="text-[11px] text-slate-500 mt-1">
              Developed for Smart India Hackathon 2026 • Legal Metrology Act 2009 & Packaged Commodities Rules 2011 Compliance.
            </p>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <button onClick={() => handleNavigate('rules')} className="text-slate-300 hover:text-white">
              Rule Knowledge Base (40 PDFs)
            </button>
            <span>•</span>
            <button onClick={() => handleNavigate('audit')} className="text-slate-300 hover:text-white">
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
