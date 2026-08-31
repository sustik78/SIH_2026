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
          <h1 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
            Enforcement Audit Trail & Security Logs
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Tamper-evident record of scans, regulatory decisions, reports generated, and supervisory actions.
          </p>
        </div>
      </div>

      {/* Search Filter */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-3">
        <Search className="w-4 h-4 text-slate-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter audit entries by officer, action, or inspection ID..."
          className="w-full text-xs bg-transparent border-0 focus:ring-0 font-medium"
        />
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs font-semibold text-slate-500">
            Loading immutable audit logs...
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500">
            No audit logs found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-600 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="p-3.5">Timestamp (IST)</th>
                  <th className="p-3.5">Officer / User</th>
                  <th className="p-3.5">Action Event</th>
                  <th className="p-3.5">Entity / Ref ID</th>
                  <th className="p-3.5">Event Details</th>
                  <th className="p-3.5 text-right">IP Address</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700 font-mono text-[11px]">
                {filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="p-3.5 text-slate-500 whitespace-nowrap">{log.timestamp}</td>
                    <td className="p-3.5 font-bold text-slate-900 font-sans">{log.username}</td>
                    <td className="p-3.5">
                      <span className="bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded text-[10px] font-bold">
                        {log.action}
                      </span>
                    </td>
                    <td className="p-3.5 text-slate-800 font-semibold">{log.entity_id || '—'}</td>
                    <td className="p-3.5 text-slate-600 font-sans text-xs">{log.details}</td>
                    <td className="p-3.5 text-right text-slate-400">{log.ip_address}</td>
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
