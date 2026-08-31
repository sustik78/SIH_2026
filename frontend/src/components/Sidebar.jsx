import React from 'react';
import { 
  LayoutDashboard, 
  ScanLine, 
  ClipboardCheck, 
  Package, 
  BookOpenCheck, 
  ShieldAlert, 
  History, 
  FileText,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export const Sidebar = ({ currentTab, onNavigate }) => {
  const navItems = [
    { id: 'dashboard', label: 'Enforcement Dashboard', icon: LayoutDashboard, badge: null },
    { id: 'scan', label: 'Scan Packaging (Studio)', icon: ScanLine, badge: 'AI Live', badgeColor: 'bg-blue-600' },
    { id: 'inspections', label: 'Inspections & Audits', icon: ClipboardCheck, badge: null },
    { id: 'products', label: 'Product Repository', icon: Package, badge: null },
    { id: 'rules', label: 'Rule Library (40 PDFs)', icon: BookOpenCheck, badge: '12 Rules', badgeColor: 'bg-amber-600' },
    { id: 'audit', label: 'Audit Trail & Logs', icon: History, badge: null },
  ];

  return (
    <aside className="w-64 bg-[#0B192C] text-slate-300 border-r border-slate-800 flex flex-col justify-between shrink-0 shadow-lg min-h-[calc(100vh-4rem)]">
      {/* Navigation list */}
      <div className="p-3 space-y-1">
        <div className="px-3 py-2 text-[11px] font-bold text-slate-300 uppercase tracking-wider">
          Enforcement Menu
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-900/50 font-semibold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] text-white px-2 py-0.5 rounded-full font-semibold ${item.badgeColor}`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}

        {/* 2-Minute Demo Mode Box */}
        <div className="pt-4 mt-4 border-t border-slate-800">
          <div className="p-3 bg-gradient-to-br from-indigo-950/80 to-blue-950/80 rounded-xl border border-blue-800/40 text-xs">
            <div className="flex items-center gap-2 text-amber-400 font-bold mb-1">
              <Sparkles className="w-4 h-4" />
              <span>SIH 2026 Judge Demo</span>
            </div>
            <p className="text-slate-300 text-[11px] leading-relaxed mb-3">
              Experience the end-to-end Legal Metrology verification pipeline in 2 minutes.
            </p>
            <button
              onClick={() => onNavigate('scan')}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white py-1.5 px-3 rounded-lg font-semibold text-xs flex items-center justify-center gap-1 shadow"
            >
              <span>Launch Quick Scan</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Dataset & Regulatory Compliance Status Footer */}
      <div className="p-4 border-t border-slate-800 bg-[#07111E] text-[11px] text-slate-300">
        <div className="font-semibold text-slate-200 mb-1 flex items-center gap-1.5">
          <BookOpenCheck className="w-3.5 h-3.5 text-amber-400" />
          <span>Statutory Authority</span>
        </div>
        <p className="text-slate-300 leading-snug">
          Legal Metrology Act, 2009 & Packaged Commodities Rules, 2011 (40 Dataset Gazettes Indexed).
        </p>
      </div>
    </aside>
  );
};
