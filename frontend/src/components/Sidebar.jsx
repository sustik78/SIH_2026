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
    { id: 'scan', label: 'Scan Packaging', icon: ScanLine, badge: 'AI Live', badgeColor: 'bg-emerald-600' },
    { id: 'inspections', label: 'Inspections & Audits', icon: ClipboardCheck, badge: null },
    { id: 'products', label: 'Product Repository', icon: Package, badge: null },
    { id: 'rules', label: 'Rule Library', icon: BookOpenCheck, badge: '40 PDFs', badgeColor: 'bg-amber-600' },
    { id: 'audit', label: 'Audit Trail & Logs', icon: History, badge: null },
  ];

  return (
    <aside className="w-72 bg-[#0B1B33] text-slate-200 border-r border-slate-800/90 flex flex-col justify-between shrink-0 shadow-lg min-h-[calc(100vh-4rem)] select-none">
      {/* Navigation list */}
      <div className="p-3.5 space-y-1.5">
        <div className="px-3 py-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
          Enforcement Menu
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? 'bg-[#2563EB] text-white shadow-md shadow-blue-950/40 font-semibold'
                  : 'text-slate-200 hover:text-white hover:bg-slate-800/80'
              }`}
            >
              <div className="flex items-center gap-3 min-w-0">
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-300'}`} />
                <span className="font-medium whitespace-nowrap">{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] text-white px-2 py-0.5 rounded-full font-bold shrink-0 ml-2 shadow-xs ${item.badgeColor}`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}

        {/* Quick Demo Workflow Box */}
        <div className="pt-3 mt-3 border-t border-slate-800/80">
          <div className="p-3 bg-gradient-to-br from-[#0F2342] to-[#16335C] rounded-xl border border-blue-700/40 text-xs">
            <div className="flex items-center gap-2 text-amber-400 font-bold mb-1">
              <Sparkles className="w-4 h-4 shrink-0" />
              <span>SIH 2026 Live Demo</span>
            </div>
            <p className="text-slate-200 text-xs leading-relaxed mb-3">
              Test end-to-end Legal Metrology verification pipeline on sample packages.
            </p>
            <button
              onClick={() => onNavigate('scan')}
              className="w-full bg-[#2563EB] hover:bg-blue-500 text-white py-2 px-3 rounded-lg font-semibold text-xs flex items-center justify-center gap-1.5 shadow transition-all"
            >
              <span>Launch Studio Scan</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Statutory Authority Status Footer */}
      <div className="p-3.5 border-t border-slate-800 bg-[#07111E] text-xs text-slate-300">
        <div className="font-semibold text-slate-100 mb-1 flex items-center gap-1.5">
          <BookOpenCheck className="w-4 h-4 text-amber-400 shrink-0" />
          <span>Statutory Authority</span>
        </div>
        <p className="text-slate-300 text-xs leading-snug">
          Legal Metrology Act 2009 & Packaged Commodities Rules 2011 (40 Gazette Acts Indexed).
        </p>
      </div>
    </aside>
  );
};
