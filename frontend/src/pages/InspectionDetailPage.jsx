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
  ChevronUp,
  Apple,
  Layers,
  Award,
  Activity,
  AlertTriangle,
  Info,
  Check,
  HeartPulse,
  Scale
} from 'lucide-react';

export const InspectionDetailPage = ({ inspectionId, onBack }) => {
  const { user } = useAuth();
  const { speakText } = useAccessibility();
  
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('label-compliance'); // 'label-compliance', 'nutrition', 'violations', 'evidence', 'report', 'overview', 'supervisory'
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
      <div className="flex flex-col items-center justify-center p-20 space-y-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-semibold text-slate-700">Loading statutory inspection records...</p>
        <p className="text-xs text-slate-400">Verifying Legal Metrology rules and extracted nutrition facts...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-10 bg-white rounded-3xl border border-slate-200 text-center space-y-4 max-w-lg mx-auto my-12 shadow-sm">
        <AlertCircle className="w-14 h-14 text-rose-600 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Inspection Record Not Found</h3>
        <p className="text-xs text-slate-500">{error || 'Unable to retrieve details.'}</p>
        <button
          onClick={onBack}
          className="px-5 py-2.5 bg-blue-700 hover:bg-blue-800 text-white text-xs font-bold rounded-xl shadow transition-all"
        >
          Return to Inspections List
        </button>
      </div>
    );
  }

  const isCompliant = data.compliance_status === 'COMPLIANT';
  const isNonCompliant = data.compliance_status === 'NON-COMPLIANT';
  const violationsList = data.violations || [];
  const nutrition = data.nutrition || {};
  const healthAssessment = data.health_classification || {
    classification: 'INSUFFICIENT DATA',
    score: 50,
    badge_color: 'slate',
    summary: 'Nutritional panel was not detected on the scanned package surface.',
    positive_factors: [],
    risk_factors: [],
    disclaimer: 'AI-derived informational assessment based on visible package declarations. Not a medical diagnosis.'
  };

  const tabs = [
    { id: 'label-compliance', label: 'Label Compliance', icon: Scale, count: `${data.passed_count}/${(data.results || []).length}` },
    { id: 'nutrition', label: 'Nutrition', icon: Apple, badge: healthAssessment.classification, badgeColor: healthAssessment.badge_color },
    { id: 'violations', label: 'Violations', icon: AlertCircle, count: violationsList.length, alert: violationsList.length > 0 },
    { id: 'evidence', label: 'Evidence', icon: Layers, count: null },
    { id: 'report', label: 'Report', icon: FileText, count: null },
    { id: 'overview', label: 'Score Overview', icon: Activity, count: null },
    { id: 'supervisory', label: 'Sign-off', icon: MessageSquare, count: null },
  ];

  return (
    <div className="space-y-6 pb-20">
      {/* 5-Stage Automated Inspection Pipeline Summary */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
          <span>Inspection Verification Pipeline</span>
          <span className="text-emerald-700 font-mono font-bold flex items-center gap-1">
            <Check className="w-3.5 h-3.5" />
            <span>AI Pipeline Complete</span>
          </span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-center text-xs">
          {[
            { step: '01', title: 'Upload', desc: 'Package Captured', done: true },
            { step: '02', title: 'OCR 5.4', desc: `${data.ocr_confidence}% Confidence`, done: true },
            { step: '03', title: 'Extraction', desc: `${(data.declarations || []).length} Declarations`, done: true },
            { step: '04', title: 'Rule Validation', desc: '12 PCR Groups', done: true },
            { step: '05', title: 'Result & Report', desc: `${data.overall_score}/100 Score`, done: true, active: true }
          ].map((p, idx) => (
            <div key={idx} className={`p-2.5 rounded-xl border text-left ${
              p.active 
                ? 'bg-blue-600 text-white border-blue-600 shadow-sm' 
                : 'bg-emerald-50/70 border-emerald-200 text-slate-800'
            }`}>
              <div className="flex items-center justify-between mb-0.5">
                <span className={`text-[10px] font-mono font-bold px-1.5 py-0.2 rounded ${
                  p.active ? 'bg-white/20 text-white' : 'bg-emerald-200 text-emerald-900'
                }`}>
                  {p.step}
                </span>
                <span className={`text-[9px] font-bold uppercase ${p.active ? 'text-blue-100' : 'text-emerald-700'}`}>
                  {p.active ? 'ACTIVE' : 'DONE'}
                </span>
              </div>
              <div className={`text-xs font-bold truncate ${p.active ? 'text-white' : 'text-slate-900'}`}>{p.title}</div>
              <div className={`text-[11px] truncate ${p.active ? 'text-blue-100' : 'text-slate-500'}`}>{p.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Action Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-700 hover:text-slate-900 bg-white px-4 py-2.5 rounded-xl border border-slate-200 shadow-sm transition-all hover:bg-slate-50"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Inspections</span>
        </button>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleDownloadPDF}
            className="px-4 py-2.5 bg-blue-700 hover:bg-blue-800 text-white text-xs font-bold rounded-xl shadow-sm flex items-center gap-1.5 transition-all shadow-blue-900/20 hover:scale-[1.02]"
          >
            <FileDown className="w-4 h-4" />
            <span>Download Official PDF</span>
          </button>

          <button
            onClick={handleDownloadDOCX}
            className="px-4 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl shadow-sm flex items-center gap-1.5 transition-all hover:scale-[1.02]"
          >
            <FileText className="w-4 h-4" />
            <span>Export DOCX (Word)</span>
          </button>
        </div>
      </div>

      {/* Main Inspection Banner Card */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/90 shadow-sm grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <div className="lg:col-span-8 space-y-3.5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold bg-blue-50 text-blue-900 px-2.5 py-1 rounded-lg border border-blue-200">
              {data.inspection_id}
            </span>
            <span className="text-xs font-semibold text-slate-400">•</span>
            <span className="text-xs font-medium text-slate-500">{data.created_at}</span>
            <span className="text-xs font-semibold text-slate-400">•</span>
            <span className="text-xs font-bold text-blue-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
              {data.category}
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-heading tracking-tight">
            {data.product_name}
          </h1>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 text-xs space-y-2">
            <div className="flex items-start gap-2">
              <span className="font-bold text-slate-900 shrink-0">Regulatory Decision:</span>
              <span className="text-slate-700 leading-relaxed">{data.decision_summary}</span>
            </div>
            <div className="flex items-start gap-2 pt-2 border-t border-slate-200">
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

      {/* Navigation Tab Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-1.5 shadow-sm flex items-center gap-1.5 overflow-x-auto scrollbar-none">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                speakText(`Showing ${tab.label} section`);
              }}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shrink-0 select-none ${
                isActive
                  ? 'bg-blue-700 text-white shadow-md shadow-blue-900/30'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
              {tab.count !== null && (
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono font-bold ${
                  isActive ? 'bg-white/20 text-white' : tab.alert ? 'bg-rose-100 text-rose-800' : 'bg-slate-200 text-slate-700'
                }`}>
                  {tab.count}
                </span>
              )}
              {tab.badge && (
                <span className={`text-[9px] px-1.5 py-0.2 rounded-full font-bold uppercase tracking-wider ${
                  isActive 
                    ? 'bg-white/20 text-white' 
                    : tab.badgeColor === 'emerald' 
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' 
                      : tab.badgeColor === 'rose'
                        ? 'bg-rose-100 text-rose-800 border border-rose-300'
                        : 'bg-amber-100 text-amber-800 border border-amber-300'
                }`}>
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* ========================================================
          TAB 1: OVERVIEW
      ======================================================== */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Quick Metrics Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <div className="text-[11px] font-bold text-slate-500 uppercase">Passed Declarations</div>
              <div className="text-2xl font-extrabold text-emerald-600 font-['Outfit'] mt-1">
                {data.passed_count}
              </div>
              <div className="text-[10px] text-slate-400">Rule 6 PCR 2011 Compliant</div>
            </div>

            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <div className="text-[11px] font-bold text-slate-500 uppercase">Violations Detected</div>
              <div className="text-2xl font-extrabold text-rose-600 font-['Outfit'] mt-1">
                {data.violation_count}
              </div>
              <div className="text-[10px] text-slate-400">Infractions requiring notice</div>
            </div>

            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <div className="text-[11px] font-bold text-slate-500 uppercase">OCR Confidence</div>
              <div className="text-2xl font-extrabold text-blue-600 font-['Outfit'] mt-1">
                {data.ocr_confidence}%
              </div>
              <div className="text-[10px] text-slate-400">Tesseract 5.4 Engine</div>
            </div>

            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
              <div className="text-[11px] font-bold text-slate-500 uppercase">Nutritional Profile</div>
              <div className={`text-base font-extrabold font-['Outfit'] mt-1 truncate ${
                healthAssessment.badge_color === 'emerald' ? 'text-emerald-600' : healthAssessment.badge_color === 'rose' ? 'text-rose-600' : 'text-amber-600'
              }`}>
                {healthAssessment.classification}
              </div>
              <div className="text-[10px] text-slate-400">Informational Assessment</div>
            </div>
          </div>

          {/* Weighted Regulatory Category Scores */}
          {data.category_scores && data.category_scores.length > 0 && (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4 flex items-center justify-between">
                <span>Weighted Regulatory Category Scores</span>
                <span className="text-slate-400 font-normal">PCR 2011 Weighted Model</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                {data.category_scores.map((cat, idx) => (
                  <div key={idx} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                    <div className="text-[11px] font-semibold text-slate-700 mb-1 truncate">{cat.name}</div>
                    <div className="flex items-baseline justify-between mb-2">
                      <span className="text-xl font-extrabold text-slate-900 font-['Outfit']">{cat.score}</span>
                      <span className="text-[10px] text-slate-400 font-bold">Max: {cat.max_score}</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
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

          {/* Side by side Preview */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left: Visual Evidence snapshot */}
            <div className="lg:col-span-6 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Scanned Package Evidence
                </h3>
                <button
                  onClick={() => setActiveTab('evidence')}
                  className="text-xs text-blue-700 font-bold hover:underline"
                >
                  Open Full Evidence Viewer ➔
                </button>
              </div>
              <div className="h-64 bg-slate-950 rounded-xl flex items-center justify-center p-2 overflow-hidden">
                <img
                  src={data.annotated_image_url || data.image_url}
                  alt={data.product_name}
                  className="max-h-full max-w-full object-contain rounded-lg"
                />
              </div>
            </div>

            {/* Right: Nutrition & Health Preview Card */}
            <div className="lg:col-span-6 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                    <Apple className="w-4 h-4 text-emerald-600" />
                    <span>Nutritional Values & Health Indicator</span>
                  </h3>
                  <button
                    onClick={() => setActiveTab('nutrition')}
                    className="text-xs text-blue-700 font-bold hover:underline"
                  >
                    View Nutrition Tab ➔
                  </button>
                </div>

                <div className={`p-4 rounded-xl border mb-3 ${
                  healthAssessment.badge_color === 'emerald' 
                    ? 'bg-emerald-50/70 border-emerald-200' 
                    : healthAssessment.badge_color === 'rose'
                      ? 'bg-rose-50/70 border-rose-200'
                      : 'bg-amber-50/70 border-amber-200'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-bold text-slate-900">Health Indicator Assessment:</span>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${
                      healthAssessment.badge_color === 'emerald'
                        ? 'bg-emerald-600 text-white border-emerald-700'
                        : healthAssessment.badge_color === 'rose'
                          ? 'bg-rose-600 text-white border-rose-700'
                          : 'bg-amber-600 text-white border-amber-700'
                    }`}>
                      {healthAssessment.classification}
                    </span>
                  </div>
                  <p className="text-xs text-slate-700 leading-relaxed mt-1">
                    {healthAssessment.summary}
                  </p>
                </div>

                {/* Key detected items pill list */}
                <div className="grid grid-cols-3 gap-2 text-center text-xs">
                  <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
                    <div className="text-[10px] text-slate-400">Energy</div>
                    <div className="font-bold text-slate-800">{nutrition?.energy?.value || 'Not detected'}</div>
                  </div>
                  <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
                    <div className="text-[10px] text-slate-400">Protein</div>
                    <div className="font-bold text-slate-800">{nutrition?.protein?.value || 'Not detected'}</div>
                  </div>
                  <div className="p-2 bg-slate-50 rounded-lg border border-slate-200">
                    <div className="text-[10px] text-slate-400">Sodium</div>
                    <div className="font-bold text-slate-800">{nutrition?.sodium?.value || 'Not detected'}</div>
                  </div>
                </div>
              </div>

              <div className="text-[10px] text-slate-400 text-center">
                Strict separation: Legal Metrology statutory compliance is evaluated independently from nutritional facts.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================
          TAB 2: LABEL COMPLIANCE (Legal Metrology PCR 2011)
      ======================================================== */}
      {activeTab === 'label-compliance' && (
        <div className="space-y-6">
          {/* Mandatory Declarations Table (Rule 6) */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-5 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 className="text-sm font-bold text-slate-900">
                  Mandatory Packaging Declarations Audit (Rule 6, PCR 2011)
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Extracted via OpenCV Preprocessing & Tesseract 5.4 OCR, verified against statutory Legal Metrology requirements.
                </p>
              </div>
              <span className="text-xs font-bold text-blue-800 bg-blue-50 px-3 py-1 rounded-lg border border-blue-200">
                Rule 6 Legal Audit
              </span>
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
                      <td className="p-3.5 font-medium">{decl.detected_value || '— Not Detected on Package —'}</td>
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
            <div className="p-5 bg-slate-50 border-b border-slate-200">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <BookOpenCheck className="w-4 h-4 text-blue-700" />
                <span>Deterministic Legal Metrology Rule Evaluations ({(data.results || []).length} Rules Checked)</span>
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Every rule links directly to the Legal Metrology Act 2009 & Packaged Commodities Rules 2011 dataset.
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
        </div>
      )}

      {/* ========================================================
          TAB 3: NUTRITIONAL VALUES (SEPARATE INFORMATIONAL TAB)
      ======================================================== */}
      {activeTab === 'nutrition' && (
        <div className="space-y-6">
          {/* Header Banner with Legal vs Nutrition Separation Notice */}
          <div className="bg-gradient-to-r from-[#0B1B33] to-[#1E3E62] text-white p-6 rounded-3xl border border-slate-700 shadow-md">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="space-y-1 max-w-2xl">
                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold uppercase tracking-wider border border-blue-400/30">
                  <Apple className="w-3.5 h-3.5 text-blue-300" />
                  <span>Informational Health Fact Extraction</span>
                </div>
                <h2 className="text-xl sm:text-2xl font-extrabold font-heading text-white">
                  Nutritional Facts & Health Classification
                </h2>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Extracted strictly from the packaging image via OCR. No values are fabricated or assumed. Undetected values are explicitly marked as <em>"Not detected from package"</em>.
                </p>
              </div>

              {/* Health Badge Card */}
              <div className="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 text-center min-w-[200px]">
                <div className="text-[10px] uppercase font-bold text-emerald-300 tracking-wider">Health Indicator</div>
                <div className={`text-lg font-extrabold font-['Outfit'] mt-0.5 ${
                  healthAssessment.badge_color === 'emerald' 
                    ? 'text-emerald-400' 
                    : healthAssessment.badge_color === 'rose'
                      ? 'text-rose-400'
                      : 'text-amber-400'
                }`}>
                  {healthAssessment.classification}
                </div>
                <div className="text-[10px] text-slate-300 mt-0.5">Score: {healthAssessment.score}/100</div>
              </div>
            </div>
          </div>

          {/* Health Assessment Detail Card */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                <HeartPulse className="w-4 h-4 text-rose-600" />
                <span>AI Informational Health Classification Analysis</span>
              </h3>
              <span className="text-[10px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                ICMR / FSSAI Reference Standard
              </span>
            </div>

            <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3.5 rounded-xl border border-slate-200/80">
              {healthAssessment.summary}
            </p>

            {/* Positive vs Risk Factors */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Positive Factors */}
              <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/40 space-y-2">
                <div className="text-xs font-bold text-emerald-900 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Favorable Nutritional Attributes</span>
                </div>
                {healthAssessment.positive_factors && healthAssessment.positive_factors.length > 0 ? (
                  <ul className="space-y-1.5 text-xs text-emerald-800">
                    {healthAssessment.positive_factors.map((pos, idx) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="font-bold text-emerald-600">•</span>
                        <span>{pos}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-slate-500 italic">No specific positive claims detected.</p>
                )}
              </div>

              {/* Risk Factors */}
              <div className="p-4 rounded-xl border border-rose-200 bg-rose-50/40 space-y-2">
                <div className="text-xs font-bold text-rose-900 flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-rose-600" />
                  <span>Nutrients of Health Concern</span>
                </div>
                {healthAssessment.risk_factors && healthAssessment.risk_factors.length > 0 ? (
                  <ul className="space-y-1.5 text-xs text-rose-800">
                    {healthAssessment.risk_factors.map((risk, idx) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="font-bold text-rose-600">•</span>
                        <span>{risk}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-emerald-700 italic">No high-risk nutrient levels detected above dietary warning thresholds.</p>
                )}
              </div>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-slate-500 flex items-center gap-2">
              <Info className="w-4 h-4 text-blue-600 shrink-0" />
              <span>
                <strong>Statutory Disclaimer:</strong> {healthAssessment.disclaimer || 'Informational assessment based strictly on visible package text. Not a medical diagnosis or dietary advice.'}
              </span>
            </div>
          </div>

          {/* Extracted Nutritional Facts Table */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-slate-900">
                  Extracted Nutritional Facts Table
                </h3>
                <p className="text-xs text-slate-500">
                  Basis: <strong>{nutrition?.serving_size?.value || 'Per 100g / 100ml'}</strong>
                </p>
              </div>
              <span className="text-[10px] font-semibold text-slate-600 bg-white border border-slate-200 px-2.5 py-1 rounded-lg">
                Deterministic OCR Reading
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-100 text-slate-600 font-bold uppercase tracking-wider text-[10px]">
                  <tr>
                    <th className="p-3.5">Nutrient Field</th>
                    <th className="p-3.5">Detected Value</th>
                    <th className="p-3.5">Status</th>
                    <th className="p-3.5">Standard Reference Unit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-700">
                  {[
                    { label: 'Energy / Calories', key: 'energy', unit: 'kcal' },
                    { label: 'Protein', key: 'protein', unit: 'g' },
                    { label: 'Total Carbohydrates', key: 'carbohydrates', unit: 'g' },
                    { label: 'Total Sugars', key: 'sugars', unit: 'g' },
                    { label: 'Added Sugars', key: 'added_sugars', unit: 'g' },
                    { label: 'Dietary Fiber', key: 'fiber', unit: 'g' },
                    { label: 'Total Fat', key: 'fat', unit: 'g' },
                    { label: 'Saturated Fat', key: 'saturated_fat', unit: 'g' },
                    { label: 'Trans Fat', key: 'trans_fat', unit: 'g' },
                    { label: 'Sodium / Salt', key: 'sodium', unit: 'mg' },
                    { label: 'Cholesterol', key: 'cholesterol', unit: 'mg' },
                  ].map((field, idx) => {
                    const obj = nutrition[field.key];
                    const isFound = Boolean(obj && obj.found);
                    return (
                      <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                        <td className="p-3.5 font-bold text-slate-900">{field.label}</td>
                        <td className="p-3.5 font-semibold">
                          {isFound ? (
                            <span className="text-slate-900">{obj.value}</span>
                          ) : (
                            <span className="text-slate-400 italic">Not detected from package</span>
                          )}
                        </td>
                        <td className="p-3.5">
                          <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                            isFound 
                              ? 'bg-emerald-50 text-emerald-800 border border-emerald-300' 
                              : 'bg-slate-100 text-slate-500 border border-slate-200'
                          }`}>
                            {isFound ? 'DETECTED' : 'NOT DETECTED'}
                          </span>
                        </td>
                        <td className="p-3.5 font-mono text-slate-500">{field.unit}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================
          TAB 4: VIOLATIONS & INFRACTIONS
      ======================================================== */}
      {activeTab === 'violations' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900">
                Regulatory Infractions & Non-Compliance Notices
              </h3>
              <p className="text-xs text-slate-500">
                Actionable violations under Legal Metrology Act, 2009 & Packaged Commodities Rules 2011.
              </p>
            </div>
            <span className={`px-3 py-1 rounded-full text-xs font-bold ${
              violationsList.length > 0 ? 'bg-rose-100 text-rose-800 border border-rose-300' : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
            }`}>
              {violationsList.length} Violation(s) Found
            </span>
          </div>

          {violationsList.length === 0 ? (
            <div className="p-12 bg-white rounded-2xl border border-slate-200 text-center space-y-3 shadow-sm">
              <CheckCircle2 className="w-12 h-12 text-emerald-600 mx-auto" />
              <h4 className="text-base font-bold text-slate-900">No Legal Metrology Violations Detected</h4>
              <p className="text-xs text-slate-500 max-w-md mx-auto">
                The product satisfies mandatory Legal Metrology declarations including metric net quantity, MRP tax clause, manufacturer information, and consumer care redressal under PCR 2011.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {violationsList.map((v, idx) => {
                const isCrit = v.severity === 'CRITICAL';
                return (
                  <div
                    key={idx}
                    className={`bg-white p-5 rounded-2xl border transition-all shadow-sm ${
                      isCrit ? 'border-red-300 bg-red-50/20' : 'border-rose-200 bg-rose-50/20'
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <span className={`px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider text-white ${
                          isCrit ? 'bg-red-700' : 'bg-rose-600'
                        }`}>
                          {v.severity} INFRACTION
                        </span>
                        <span className="font-mono text-xs font-bold text-slate-900">{v.rule_id}</span>
                        <h4 className="text-sm font-bold text-slate-900">{v.violation_title}</h4>
                      </div>
                      <span className="text-[11px] font-semibold text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                        {v.legal_basis}
                      </span>
                    </div>

                    <p className="text-xs text-slate-700 leading-relaxed mb-3">
                      {v.description}
                    </p>

                    <div className="p-2.5 bg-white rounded-xl border border-slate-200 text-xs flex items-center justify-between">
                      <div>
                        <span className="font-bold text-slate-800">Detected Value on Package: </span>
                        <span className="text-slate-600">{v.detected_value || 'Omitted / Missing'}</span>
                      </div>
                      <span className="text-[10px] text-rose-700 font-semibold">
                        Action: Notice Under Section 36(1)
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* ========================================================
          TAB 5: VISUAL EVIDENCE
      ======================================================== */}
      {activeTab === 'evidence' && (
        <div className="space-y-6">
          <EvidenceViewer
            originalImageUrl={data.image_url}
            annotatedImageUrl={data.annotated_image_url}
            results={data.results}
          />

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
        </div>
      )}

      {/* ========================================================
          TAB 6: OFFICIAL REPORT
      ======================================================== */}
      {activeTab === 'report' && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Government Statutory Inspection Report
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Official evidence document formatted for the Directorate of Legal Metrology & court proceedings.
                </p>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={handleDownloadPDF}
                  className="px-5 py-2.5 bg-blue-700 hover:bg-blue-800 text-white text-xs font-bold rounded-xl shadow flex items-center gap-2 transition-all"
                >
                  <FileDown className="w-4 h-4" />
                  <span>Download Signed PDF</span>
                </button>

                <button
                  onClick={handleDownloadDOCX}
                  className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl shadow flex items-center gap-2 transition-all"
                >
                  <FileText className="w-4 h-4" />
                  <span>Download Word (.DOCX)</span>
                </button>
              </div>
            </div>

            {/* Document Preview Box */}
            <div className="border border-slate-200 rounded-2xl p-6 bg-slate-50 text-slate-800 space-y-4 text-xs font-serif">
              <div className="text-center space-y-1 pb-3 border-b border-slate-200">
                <div className="font-bold text-slate-900 text-sm">GOVERNMENT OF INDIA</div>
                <div className="font-semibold text-slate-700">MINISTRY OF CONSUMER AFFAIRS, FOOD & PUBLIC DISTRIBUTION</div>
                <div className="text-[11px] text-slate-500">LEGAL METROLOGY DIVISION — PACKAGED COMMODITIES RULES, 2011</div>
                <div className="text-[10px] font-mono text-blue-900 font-bold mt-1">
                  REPORT REF: {data.inspection_id}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] font-sans">
                <div><strong>Product:</strong> {data.product_name}</div>
                <div><strong>Category:</strong> {data.category}</div>
                <div><strong>Inspecting Officer:</strong> {data.inspector_name}</div>
                <div><strong>Date of Audit:</strong> {data.created_at}</div>
                <div><strong>Overall Score:</strong> {data.overall_score}/100</div>
                <div><strong>Compliance Status:</strong> <strong className={isCompliant ? 'text-emerald-700' : 'text-rose-700'}>{data.compliance_status}</strong></div>
              </div>

              <div className="font-sans pt-2 border-t border-slate-200 text-xs">
                <div className="font-bold text-slate-900 mb-1">Statutory Finding & Action:</div>
                <p className="text-slate-700 leading-relaxed">{data.decision_summary}</p>
                <p className="text-blue-900 font-semibold mt-1">{data.recommended_action}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================
          TAB 7: SUPERVISORY REVIEW & SIGN-OFF
      ======================================================== */}
      {activeTab === 'supervisory' && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-blue-700" />
              <h3 className="text-sm font-bold text-slate-900">
                Supervisory Review & Statutory Endorsement
              </h3>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Official Supervisory Notes & Action Order
              </label>
              <textarea
                rows={4}
                value={supervisorNotes}
                onChange={(e) => setSupervisorNotes(e.target.value)}
                placeholder="Enter supervisory verification remarks, notice dispatch date, compounding orders, or penalty references..."
                className="w-full text-xs p-3.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all font-medium text-slate-900"
              />
            </div>

            <div className="flex flex-wrap items-center justify-end gap-3 pt-2">
              <button
                onClick={() => handleUpdateStatus('FLAGGED')}
                disabled={isUpdatingStatus}
                className="px-4 py-2.5 bg-rose-50 hover:bg-rose-100 text-rose-800 text-xs font-bold rounded-xl border border-rose-300 transition-colors"
              >
                Flag for Seizure / Section 36 Notice
              </button>
              <button
                onClick={() => handleUpdateStatus('UNDER_REVIEW')}
                disabled={isUpdatingStatus}
                className="px-4 py-2.5 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-bold rounded-xl border border-amber-300 transition-colors"
              >
                Mark Under Investigation
              </button>
              <button
                onClick={() => handleUpdateStatus('APPROVED')}
                disabled={isUpdatingStatus}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow transition-colors"
              >
                Approve & Endorse Inspection
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
