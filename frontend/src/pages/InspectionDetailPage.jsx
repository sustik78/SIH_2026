import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useAccessibility } from '../context/AccessibilityContext';
import { apiGetJson, apiFetch } from '../utils/api';
import { ScoreGauge } from '../components/ScoreGauge';
import { EvidenceViewer } from '../components/EvidenceViewer';
import { 
  FileDown, 
  ArrowLeft, 
  ShieldAlert, 
  ShieldCheck, 
  AlertCircle, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  BookOpenCheck, 
  FileText, 
  MessageSquare,
  Sparkles,
  ExternalLink,
  Printer,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export const InspectionDetailPage = ({ inspectionId, onBack }) => {
  const { user } = useAuth();
  const { speakText } = useAccessibility();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [supervisorNotes, setSupervisorNotes] = useState('');
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);
  const [showRawOcr, setShowRawOcr] = useState(false);

  useEffect(() => {
    if (inspectionId) {
      fetchInspection();
    }
  }, [inspectionId]);

  const fetchInspection = async () => {
    try {
      setLoading(true);
      setError('');
      const result = await apiGetJson(`/api/inspections/${inspectionId}`);
      setData(result);
      setSupervisorNotes(result.supervisor_notes || '');
    } catch (e) {
      console.error('Inspection fetch error:', e);
      setError(e.message || 'Inspection details could not be loaded.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (newStatus) => {
    try {
      setIsUpdatingStatus(true);
      const res = await apiFetch(`/api/inspections/${inspectionId}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus, supervisor_notes: supervisorNotes })
      });
      if (res.ok) {
        await fetchInspection();
        speakText(`Inspection marked as ${newStatus}`);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  const handleDownloadPDF = () => {
    window.open(`/api/reports/${inspectionId}/pdf`, '_blank');
    speakText("Downloading official statutory PDF report.");
  };

  const handleDownloadDOCX = () => {
    window.open(`/api/reports/${inspectionId}/docx`, '_blank');
    speakText("Downloading editable DOCX inspection report.");
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center p-16 space-y-4">
        <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-semibold text-slate-600">Loading statutory inspection records...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center space-y-4">
        <AlertCircle className="w-12 h-12 text-rose-600 mx-auto" />
        <h3 className="text-base font-bold text-slate-900">Inspection Record Not Found</h3>
        <p className="text-xs text-slate-500">{error || 'Unable to retrieve details.'}</p>
        <button
          onClick={onBack}
          className="px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg"
        >
          Return to Inspections
        </button>
      </div>
    );
  }

  const isCompliant = data.compliance_status === 'COMPLIANT';
  const isNonCompliant = data.compliance_status === 'NON-COMPLIANT';

  return (
    <div className="space-y-6 pb-16">
      {/* Top Action Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 bg-white px-3.5 py-2 rounded-xl border border-slate-200 shadow-sm transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to List</span>
        </button>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleDownloadPDF}
            className="px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white text-xs font-bold rounded-xl shadow-sm flex items-center gap-1.5 transition-all"
          >
            <FileDown className="w-4 h-4" />
            <span>Download Official PDF</span>
          </button>

          <button
            onClick={handleDownloadDOCX}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold rounded-xl shadow-sm flex items-center gap-1.5 transition-all"
          >
            <FileText className="w-4 h-4" />
            <span>Export DOCX (Word)</span>
          </button>
        </div>
      </div>

      {/* Main Inspection Banner Card */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <div className="lg:col-span-8 space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg border border-slate-200">
              {data.inspection_id}
            </span>
            <span className="text-xs font-semibold text-slate-400">•</span>
            <span className="text-xs font-medium text-slate-500">{data.created_at}</span>
            <span className="text-xs font-semibold text-slate-400">•</span>
            <span className="text-xs font-bold text-blue-700">{data.category}</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-['Outfit']">
            {data.product_name}
          </h1>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-xs space-y-2">
            <div className="flex items-start gap-2">
              <span className="font-bold text-slate-900 shrink-0">Regulatory Decision:</span>
              <span className="text-slate-700">{data.decision_summary}</span>
            </div>
            <div className="flex items-start gap-2 pt-1 border-t border-slate-200">
              <span className="font-bold text-slate-900 shrink-0">Statutory Recommendation:</span>
              <span className="text-blue-900 font-semibold">{data.recommended_action}</span>
            </div>
          </div>
        </div>

        {/* Right Gauge */}
        <div className="lg:col-span-4 flex justify-center">
          <ScoreGauge score={data.overall_score} status={data.compliance_status} size={150} />
        </div>
      </div>

      {/* Category Breakdown & Scores */}
      {data.category_scores && data.category_scores.length > 0 && (
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">
            Weighted Regulatory Category Scores
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            {data.category_scores.map((cat, idx) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200/80">
                <div className="text-[11px] font-semibold text-slate-600 mb-1 truncate">{cat.name}</div>
                <div className="flex items-baseline justify-between mb-1.5">
                  <span className="text-lg font-extrabold text-slate-900 font-['Outfit']">{cat.score}</span>
                  <span className="text-[10px] text-slate-400 font-bold">Max: {cat.max_score}</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      cat.percentage >= 85 ? 'bg-emerald-500' : cat.percentage >= 60 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                    style={{ width: `${cat.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Visual Evidence Viewer */}
      <EvidenceViewer
        originalImageUrl={data.image_url}
        annotatedImageUrl={data.annotated_image_url}
        results={data.results}
      />

      {/* Mandatory Declarations Table (Rule 6) */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900">
              Mandatory Packaging Declarations Audit (Rule 6, PCR 2011)
            </h3>
            <p className="text-xs text-slate-500">
              Extracted via Tesseract 5.4 OCR and verified against statutory requirements.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100 text-slate-600 font-bold uppercase tracking-wider text-[10px]">
              <tr>
                <th className="p-3.5">Declaration Field</th>
                <th className="p-3.5">Detected Value on Packaging</th>
                <th className="p-3.5">Extraction Status</th>
                <th className="p-3.5">OCR Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {(data.declarations || []).map((decl, idx) => (
                <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                  <td className="p-3.5 font-bold text-slate-900">{decl.field_name}</td>
                  <td className="p-3.5 font-medium">{decl.detected_value || '— Not Detected —'}</td>
                  <td className="p-3.5">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                      decl.is_found 
                        ? 'bg-emerald-50 text-emerald-800 border border-emerald-300' 
                        : 'bg-rose-50 text-rose-800 border border-rose-300'
                    }`}>
                      {decl.is_found ? 'FOUND' : 'MISSING'}
                    </span>
                  </td>
                  <td className="p-3.5 font-mono text-slate-600">{decl.confidence_score}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detailed Legal Metrology Rule Evaluations */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <BookOpenCheck className="w-4 h-4 text-blue-700" />
            <span>Deterministic Legal Metrology Rule Evaluations ({(data.results || []).length} Checks)</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Every evaluation links directly to the Legal Metrology Act 2009 & Packaged Commodities Rules 2011 dataset.
          </p>
        </div>

        <div className="divide-y divide-slate-100">
          {(data.results || []).map((rule, idx) => {
            const isPass = rule.status === 'PASS';
            const isWarn = rule.status === 'WARNING';
            const isFail = rule.status === 'VIOLATION';
            return (
              <div key={idx} className="p-4 hover:bg-slate-50/80 transition-colors space-y-2">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${
                      isPass 
                        ? 'bg-emerald-50 text-emerald-800 border-emerald-300' 
                        : isWarn 
                          ? 'bg-amber-50 text-amber-800 border-amber-300' 
                          : 'bg-rose-50 text-rose-800 border-rose-300'
                    }`}>
                      {rule.status}
                    </span>
                    <span className="font-mono text-xs font-bold text-blue-900">{rule.rule_id}</span>
                    <span className="text-xs font-bold text-slate-900">{rule.rule_name}</span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-medium">Category: {rule.category}</span>
                </div>

                <p className="text-xs text-slate-700 leading-relaxed pl-1">
                  {rule.explanation}
                </p>

                <div className="flex flex-wrap items-center gap-3 text-[10px] bg-slate-50 p-2 rounded-lg border border-slate-200/80 text-slate-600">
                  <div>
                    <span className="font-bold text-slate-800">Statutory Reference: </span>
                    <span className="text-blue-800 font-semibold">{rule.source_section}</span>
                  </div>
                  <span className="text-slate-300">•</span>
                  <div className="truncate max-w-sm">
                    <span className="font-bold text-slate-800">Gazette Source: </span>
                    <span className="font-mono text-slate-600">{rule.source_document}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Raw OCR Text Dropdown */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <button
          onClick={() => setShowRawOcr(!showRawOcr)}
          className="w-full p-4 bg-slate-50 flex items-center justify-between text-left text-xs font-bold text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <span>View Raw Extracted OCR Text Stream</span>
          {showRawOcr ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
        {showRawOcr && (
          <div className="p-4 bg-slate-900 text-slate-300 font-mono text-xs max-h-60 overflow-y-auto leading-relaxed border-t border-slate-800">
            {data.raw_ocr_text || 'No raw text recorded.'}
          </div>
        )}
      </div>

      {/* Supervisor Review & Endorsement Box */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-blue-700" />
          <h3 className="text-sm font-bold text-slate-900">
            Supervisory Review & Statutory Endorsement
          </h3>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
            Official Enforcement Notes / Remarks
          </label>
          <textarea
            rows={3}
            value={supervisorNotes}
            onChange={(e) => setSupervisorNotes(e.target.value)}
            placeholder="Enter supervisory verification remarks, notice dispatch date, or penalty order references..."
            className="w-full text-xs p-3 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all font-medium"
          />
        </div>

        <div className="flex flex-wrap items-center justify-end gap-3 pt-2">
          <button
            onClick={() => handleUpdateStatus('FLAGGED')}
            disabled={isUpdatingStatus}
            className="px-4 py-2 bg-rose-50 hover:bg-rose-100 text-rose-800 text-xs font-bold rounded-xl border border-rose-300 transition-colors"
          >
            Flag for Seizure / Legal Action
          </button>
          <button
            onClick={() => handleUpdateStatus('UNDER_REVIEW')}
            disabled={isUpdatingStatus}
            className="px-4 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-bold rounded-xl border border-amber-300 transition-colors"
          >
            Mark Under Investigation
          </button>
          <button
            onClick={() => handleUpdateStatus('APPROVED')}
            disabled={isUpdatingStatus}
            className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow transition-colors"
          >
            Approve & Sign-off Inspection
          </button>
        </div>
      </div>
    </div>
  );
};
