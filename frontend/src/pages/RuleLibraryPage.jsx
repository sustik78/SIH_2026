import React, { useState, useEffect } from 'react';
import { apiGetJson } from '../utils/api';
import { 
  BookOpenCheck, 
  Search, 
  Scale, 
  FileText, 
  CheckCircle2, 
  ShieldAlert, 
  AlertTriangle,
  Info,
  ExternalLink,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export const RuleLibraryPage = () => {
  const [rules, setRules] = useState([]);
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [expandedRule, setExpandedRule] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRules();
  }, [categoryFilter]);

  const fetchRules = async () => {
    try {
      setLoading(true);
      const url = categoryFilter !== 'ALL' ? `/api/rules?category=${encodeURIComponent(categoryFilter)}` : '/api/rules';
      const data = await apiGetJson(url);
      setRules(data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const filteredRules = rules.filter(r => {
    if (!search) return true;
    const s = search.toLowerCase();
    return (
      r.rule_id.toLowerCase().includes(s) ||
      r.rule_name.toLowerCase().includes(s) ||
      r.requirement.toLowerCase().includes(s) ||
      r.source_section.toLowerCase().includes(s)
    );
  });

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
          <BookOpenCheck className="w-4 h-4" />
          <span>Statutory Knowledge Base (40 Dataset Gazettes Indexed)</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
          Legal Metrology Compliance Rule Library
        </h1>
        <p className="text-xs text-slate-500 mt-1 leading-relaxed max-w-4xl">
          Deterministic compliance rules extracted directly from the <strong>Legal Metrology Act, 2009</strong> and <strong>Packaged Commodities Rules (PCR 2011 & Gazette Amendments)</strong>. Zero hallucinations: every rule is traceable to an official statutory document.
        </p>
      </div>

      {/* Search & Category Filter */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-wrap items-center gap-3">
        <div className="flex-1 min-w-[240px] relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search rules by ID, rule name, or gazette provision..."
            className="w-full text-xs pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 font-medium"
          />
        </div>

        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="text-xs px-3 py-2.5 bg-slate-50 border border-slate-300 rounded-xl font-semibold text-slate-700 cursor-pointer"
        >
          <option value="ALL">All Rule Categories</option>
          <option value="Identity & Origin">Identity & Origin</option>
          <option value="Product Identification">Product Identification</option>
          <option value="Quantity & Measurement">Quantity & Measurement</option>
          <option value="Dates & Freshness">Dates & Freshness</option>
          <option value="Pricing & Taxes">Pricing & Taxes</option>
          <option value="Consumer Protection">Consumer Protection</option>
          <option value="Display & Legibility">Display & Legibility</option>
          <option value="Exemptions & Special Provisions">Exemptions (Rule 26)</option>
        </select>
      </div>

      {/* Rules List */}
      {loading ? (
        <div className="p-12 text-center text-xs font-semibold text-slate-500">
          Loading statutory rule definitions...
        </div>
      ) : (
        <div className="space-y-4">
          {filteredRules.map((rule) => {
            const isExpanded = expandedRule === rule.rule_id;
            const isCritical = rule.severity === 'CRITICAL';
            const isHigh = rule.severity === 'HIGH';

            return (
              <div
                key={rule.rule_id}
                className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden transition-all"
              >
                <div
                  onClick={() => setExpandedRule(isExpanded ? null : rule.rule_id)}
                  className="p-5 cursor-pointer hover:bg-slate-50/80 transition-colors flex items-start justify-between gap-4"
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-xs font-bold text-blue-900 bg-blue-50 px-2.5 py-0.5 rounded border border-blue-200">
                        {rule.rule_id}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                        isCritical 
                          ? 'bg-rose-100 text-rose-800 border border-rose-300' 
                          : isHigh 
                            ? 'bg-amber-100 text-amber-800 border border-amber-300' 
                            : 'bg-slate-100 text-slate-700 border border-slate-300'
                      }`}>
                        Severity: {rule.severity}
                      </span>
                      <span className="text-xs font-semibold text-slate-400">•</span>
                      <span className="text-xs font-semibold text-slate-500">{rule.category}</span>
                    </div>

                    <h3 className="text-base font-bold text-slate-900 font-['Outfit']">
                      {rule.rule_name}
                    </h3>

                    <p className="text-xs text-slate-600 leading-relaxed line-clamp-2">
                      {rule.requirement}
                    </p>
                  </div>

                  <button className="text-slate-400 hover:text-slate-700 p-1">
                    {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </button>
                </div>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="p-5 bg-slate-50 border-t border-slate-200 space-y-4 text-xs">
                    <div>
                      <h4 className="font-bold text-slate-900 mb-1">Statutory Requirement</h4>
                      <p className="text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-200">
                        {rule.requirement}
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-bold text-slate-900 mb-1">AI Validation Logic</h4>
                        <p className="text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-200">
                          {rule.validation_logic}
                        </p>
                      </div>

                      <div>
                        <h4 className="font-bold text-slate-900 mb-1">Statutory Purpose & Rationale</h4>
                        <p className="text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-200">
                          {rule.explanation}
                        </p>
                      </div>
                    </div>

                    {/* Source citations */}
                    <div className="p-3 bg-blue-50/80 rounded-xl border border-blue-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-slate-700">
                      <div>
                        <span className="font-bold text-blue-950">Statutory Section: </span>
                        <span className="font-semibold text-blue-900">{rule.source_section}</span>
                        <span className="text-slate-400 block text-[11px] font-mono mt-0.5">
                          Dataset Source File: {rule.source_document}
                        </span>
                      </div>
                      <span className="text-[10px] font-bold text-blue-800 bg-white px-2.5 py-1 rounded-md border border-blue-200 shadow-sm shrink-0">
                        Government of India Gazette
                      </span>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
