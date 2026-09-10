import React, { useState, useEffect } from 'react';
import { apiGetJson } from '../utils/api';
import { 
  History, 
  ShieldCheck, 
  UserCheck, 
  Clock, 
  FileText, 
  ScanLine, 
  Lock, 
  Search
} from 'lucide-react';

export const AuditTrailPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const data = await apiGetJson('/api/audit/logs');
      setLogs(data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const filteredLogs = logs.filter(l => {
    if (!search) return true;
    const s = search.toLowerCase();
    return (
      l.username.toLowerCase().includes(s) ||
      l.action.toLowerCase().includes(s) ||
      l.details.toLowerCase().includes(s) ||
      l.entity_id?.toLowerCase().includes(s)
    );
  });

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
            <History className="w-4 h-4" />
            <span>Immutable Enforcement Logs</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 font-heading">
            Enforcement Audit Trail & Security Logs
          </h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Tamper-evident record of scans, regulatory decisions, reports generated, and supervisory actions.
          </p>
        </div>

        {logs.length > 0 && (
          <button
            onClick={async () => {
              if (window.confirm("Are you sure you want to clear all enforcement audit logs?")) {
                try {
                  await fetch('/api/audit/logs', { method: 'DELETE' });
                  setLogs([]);
                } catch (e) {
                  console.error(e);
                }
              }
            }}
            className="px-3.5 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-bold rounded-xl border border-rose-200 transition-colors shrink-0"
          >
            Clear Audit Trail
          </button>
        )}
      </div>

      {/* Search Filter */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-3">
        <Search className="w-4 h-4 text-slate-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter audit entries by officer, action, or inspection ID..."
          className="w-full text-xs bg-transparent border-0 focus:ring-0 font-medium text-slate-900"
        />
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs font-semibold text-slate-500">
            Loading immutable audit logs...
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="p-14 text-center space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center mx-auto text-slate-400 border border-slate-200 shadow-xs">
              <ShieldCheck className="w-6 h-6 text-slate-500" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-800">No Enforcement Logs Recorded</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                Audit trail is clean and ready. New tamper-evident log records will be automatically generated as officers execute package scans and supervisory actions.
              </p>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-700 font-bold uppercase tracking-wider text-xs border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Timestamp (IST)</th>
                  <th className="py-3 px-4">Officer / User</th>
                  <th className="py-3 px-4">Action Event</th>
                  <th className="py-3 px-4">Entity / Ref ID</th>
                  <th className="py-3 px-4">Event Details</th>
                  <th className="py-3 px-4 text-right">IP Address</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700 font-mono text-xs">
                {filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-4 text-slate-500 whitespace-nowrap">{log.timestamp}</td>
                    <td className="py-3 px-4 font-bold text-slate-900 font-sans">{log.username}</td>
                    <td className="py-3 px-4">
                      <span className="bg-blue-50 text-blue-800 border border-blue-200 px-2.5 py-0.5 rounded text-xs font-bold font-sans">
                        {log.action}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-800 font-semibold">{log.entity_id || '—'}</td>
                    <td className="py-3 px-4 text-slate-600 font-sans text-xs">{log.details}</td>
                    <td className="py-3 px-4 text-right text-slate-400">{log.ip_address}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
