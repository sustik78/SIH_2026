import React, { useState, useEffect } from 'react';
import { apiGetJson } from '../utils/api';
import { 
  ScanLine, 
  ShieldCheck, 
  AlertTriangle, 
  XCircle, 
  Clock, 
  TrendingUp, 
  CheckCircle2, 
  FileText, 
  ChevronRight,
  Filter,
  ArrowUpRight
} from 'lucide-react';

export const DashboardPage = ({ onNavigate, onSelectInspection }) => {
  const [summary, setSummary] = useState({
    total_scans: 3,
    compliant_count: 1,
    non_compliant_count: 2,
    pending_review_count: 1,
    critical_violations_count: 2,
    compliance_rate: 33.3,
    top_violations: [],
    category_breakdown: []
  });
  const [recentInspections, setRecentInspections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [sumData, inspData] = await Promise.all([
        apiGetJson('/api/analytics/summary'),
        apiGetJson('/api/inspections')
      ]);
      if (sumData) setSummary(sumData);
      if (inspData) setRecentInspections(inspData);
    } catch (e) {
      console.error('Error loading dashboard data:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>National Metrology Enforcement Directorate</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
            Enforcement & Compliance Dashboard
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time surveillance overview of packaged commodities under PCR 2011.
          </p>
        </div>

        <button
          onClick={() => onNavigate('scan')}
          className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md flex items-center gap-2 transition-all shrink-0"
        >
          <ScanLine className="w-4 h-4" />
          <span>New Product Scan</span>
        </button>
      </div>

      {/* 5 Key Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: 'TOTAL SCANNED', val: summary.total_scans, sub: 'Packaged Commodities', icon: ScanLine, color: 'text-blue-600', bg: 'bg-blue-50 border-blue-200' },
          { label: 'FULLY COMPLIANT', val: summary.compliant_count, sub: 'Passed All Rules', icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50 border-emerald-200' },
          { label: 'NON-COMPLIANT', val: summary.non_compliant_count, sub: 'Statutory Notice Req.', icon: XCircle, color: 'text-rose-600', bg: 'bg-rose-50 border-rose-200' },
          { label: 'PENDING REVIEW', val: summary.pending_review_count, sub: 'Under Supervision', icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50 border-amber-200' },
          { label: 'CRITICAL INFRACTIONS', val: summary.critical_violations_count, sub: 'Sec 36(1) Violations', icon: AlertTriangle, color: 'text-purple-600', bg: 'bg-purple-50 border-purple-200' }
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className={`p-4 rounded-2xl border ${card.bg} shadow-sm flex flex-col justify-between`}>
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600">
                  {card.label}
                </span>
                <Icon className={`w-4 h-4 ${card.color}`} />
              </div>
              <div className="my-2">
                <span className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
                  {card.val}
                </span>
              </div>
              <span className="text-[10px] text-slate-500 font-medium">{card.sub}</span>
            </div>
          );
        })}
      </div>

      {/* Middle Grid: Charts & Compliance Rates */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Overall Compliance Rate */}
        <div className="lg:col-span-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1 flex items-center justify-between">
              <span>National Compliance Rate</span>
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </h3>
            <p className="text-xs text-slate-500 mb-4">Percentage of packages complying with all mandatory rules.</p>
            
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-4xl font-extrabold text-slate-900 font-['Outfit']">
                {summary.compliance_rate}%
              </span>
              <span className="text-xs text-emerald-600 font-bold">Standard Target: 90%</span>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden border border-slate-200 mb-4">
              <div
                className={`h-full rounded-full transition-all duration-1000 ${
                  summary.compliance_rate >= 80 ? 'bg-emerald-500' : summary.compliance_rate >= 50 ? 'bg-amber-500' : 'bg-rose-500'
                }`}
                style={{ width: `${summary.compliance_rate}%` }}
              ></div>
            </div>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 space-y-1.5">
            <div className="flex justify-between">
              <span className="font-medium">Total Compliance Checks:</span>
              <span className="font-bold text-slate-900">{summary.total_scans * 12} rules evaluated</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Statutory Framework:</span>
              <span className="font-bold text-blue-700">PCR 2011 & Amendments</span>
            </div>
          </div>
        </div>

        {/* Right: Most Common Regulatory Violations */}
        <div className="lg:col-span-8 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">
              Frequent Legal Metrology Infractions Detected
            </h3>
            <p className="text-xs text-slate-500 mb-4">Rule violation frequency across inspected pre-packaged commodities.</p>

            <div className="space-y-3">
              {[
                { rule: 'LM-PCR-05', name: 'MRP Missing Statutory Tax Clause', pct: 67, color: 'bg-rose-500' },
                { rule: 'LM-PCR-07', name: 'Consumer Care Helpline / Email Omission', pct: 67, color: 'bg-rose-500' },
                { rule: 'LM-PCR-06', name: 'Unit Sale Price (USP) Missing / Miscalculated', pct: 33, color: 'bg-amber-500' },
                { rule: 'LM-PCR-03', name: 'Non-Standard Net Qty Expressions (Jumbo/Family)', pct: 33, color: 'bg-rose-600' },
                { rule: 'LM-PCR-01', name: 'Incomplete Manufacturer / Packer Address', pct: 33, color: 'bg-amber-500' }
              ].map((item, idx) => (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-semibold text-slate-800">
                      <span className="font-mono text-blue-700 mr-1.5">{item.rule}</span>
                      {item.name}
                    </span>
                    <span className="font-bold text-slate-700">{item.pct}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div className={`h-full ${item.color} rounded-full`} style={{ width: `${item.pct}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Inspections Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900">
            Recent Product Inspections
          </h3>
          <button
            onClick={() => onNavigate('inspections')}
            className="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1"
          >
            <span>View All</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100/70 text-slate-600 font-bold border-b border-slate-200 uppercase tracking-wider text-[10px]">
              <tr>
                <th className="p-3.5">Product Name</th>
                <th className="p-3.5">Inspection ID</th>
                <th className="p-3.5">Date</th>
                <th className="p-3.5">Score</th>
                <th className="p-3.5">Compliance Status</th>
                <th className="p-3.5">Inspector</th>
                <th className="p-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {recentInspections.map((insp) => {
                const isCompliant = insp.compliance_status === 'COMPLIANT';
                const isWarning = insp.compliance_status === 'PENDING REVIEW';
                return (
                  <tr key={insp.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="p-3.5 font-bold text-slate-900">
                      {insp.product_name}
                      <span className="block text-[10px] font-normal text-slate-400">{insp.category}</span>
                    </td>
                    <td className="p-3.5 font-mono text-slate-600 font-medium">{insp.inspection_id}</td>
                    <td className="p-3.5 text-slate-500">{insp.created_at}</td>
                    <td className="p-3.5">
                      <span className="font-extrabold text-slate-900 text-sm font-['Outfit']">{insp.overall_score}</span>
                      <span className="text-[10px] text-slate-400">/100</span>
                    </td>
                    <td className="p-3.5">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${
                        isCompliant 
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-300' 
                          : isWarning 
                            ? 'bg-amber-50 text-amber-800 border-amber-300' 
                            : 'bg-rose-50 text-rose-800 border-rose-300'
                      }`}>
                        {insp.compliance_status}
                      </span>
                    </td>
                    <td className="p-3.5 font-medium text-slate-800">{insp.inspector_name}</td>
                    <td className="p-3.5 text-right">
                      <button
                        onClick={() => onSelectInspection(insp.inspection_id)}
                        className="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-800 font-bold rounded-lg transition-colors inline-flex items-center gap-1"
                      >
                        <span>Open Report</span>
                        <ArrowUpRight className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
