import React, { useState, useEffect } from 'react';
import { apiGetJson } from '../utils/api';
import { 
  Search, 
  Filter, 
  FileDown, 
  Calendar, 
  ArrowUpRight, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle,
  Clock,
  ClipboardList
} from 'lucide-react';

export const InspectionHistoryPage = ({ onSelectInspection }) => {
  const [inspections, setInspections] = useState([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInspections();
  }, [statusFilter, categoryFilter]);

  const fetchInspections = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (statusFilter !== 'ALL') params.append('status', statusFilter);
      if (categoryFilter !== 'ALL') params.append('category', categoryFilter);
      if (search) params.append('search', search);

      const data = await apiGetJson(`/api/inspections?${params.toString()}`);
      setInspections(data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchInspections();
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
            <ClipboardList className="w-4 h-4" />
            <span>Inspection Repository & Search</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
            Legal Metrology Inspection History
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Complete database of statutory packaging audits conducted under PCR 2011.
          </p>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-wrap items-center gap-3">
        <form onSubmit={handleSearchSubmit} className="flex-1 min-w-[240px] relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by product, inspection ID, or officer..."
            className="w-full text-xs pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 font-medium"
          />
        </form>

        <div className="flex items-center gap-2">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="text-xs px-3 py-2.5 bg-slate-50 border border-slate-300 rounded-xl font-semibold text-slate-700 cursor-pointer"
          >
            <option value="ALL">All Compliance Statuses</option>
            <option value="COMPLIANT">Compliant</option>
            <option value="NON-COMPLIANT">Non-Compliant</option>
            <option value="PENDING REVIEW">Pending Review</option>
          </select>

          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="text-xs px-3 py-2.5 bg-slate-50 border border-slate-300 rounded-xl font-semibold text-slate-700 cursor-pointer"
          >
            <option value="ALL">All Categories</option>
            <option value="Packaged Food / Atta">Packaged Food / Atta</option>
            <option value="Edible Oils & Fats">Edible Oils & Fats</option>
            <option value="Snack Foods">Snack Foods</option>
            <option value="Readymade Garments & Hosiery">Readymade Garments</option>
          </select>
        </div>
      </div>

      {/* Inspections Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs font-semibold text-slate-500">
            Loading inspection records...
          </div>
        ) : inspections.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500">
            No inspection records match the selected filters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100/70 text-slate-600 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="p-3.5">Product Name</th>
                  <th className="p-3.5">Inspection ID</th>
                  <th className="p-3.5">Date</th>
                  <th className="p-3.5">Score</th>
                  <th className="p-3.5">Status</th>
                  <th className="p-3.5">Inspector</th>
                  <th className="p-3.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {inspections.map((insp) => {
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
        )}
      </div>
    </div>
  );
};
