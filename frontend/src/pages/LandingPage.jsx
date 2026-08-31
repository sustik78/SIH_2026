import React from 'react';
import { 
  Scale, 
  ScanLine, 
  ShieldCheck, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  ChevronRight, 
  ArrowRight,
  Database,
  Search,
  Award,
  Layers,
  Sparkles,
  BookOpenCheck,
  Zap,
  Users
} from 'lucide-react';

export const LandingPage = ({ onNavigate }) => {
  return (
    <div className="space-y-16 pb-16">
      {/* 1. Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-[#0B192C] via-[#0F2942] to-[#1E3E62] text-white rounded-3xl p-8 sm:p-12 lg:p-16 shadow-2xl border border-slate-700/50">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 -mb-12 -ml-12 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="max-w-4xl mx-auto text-center relative z-10 space-y-6">
          {/* Government Badge */}
          <div className="inline-flex items-center gap-2 bg-blue-900/60 border border-blue-400/30 px-3 py-1.5 rounded-full text-xs font-semibold tracking-wide text-blue-200 backdrop-blur-md">
            <Scale className="w-4 h-4 text-amber-400" />
            <span>Legal Metrology Enforcement System • SIH 2026</span>
          </div>

          {/* Main Title */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight font-['Outfit'] leading-tight">
            PRAMAN AI
            <span className="block text-2xl sm:text-3xl lg:text-4xl font-semibold text-blue-200 mt-2">
              Packaging Regulations & Automated Metrology Audit Network
            </span>
          </h1>

          {/* Core Tagline */}
          <p className="text-xl sm:text-2xl font-semibold text-amber-400 font-['Outfit']">
            “From Package Image to Compliance Decision.”
          </p>

          <p className="text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
            AI-powered Legal Metrology compliance inspection for faster, transparent, and evidence-backed enforcement of the <span className="text-white font-semibold">Legal Metrology Act, 2009</span> and <span className="text-white font-semibold">Packaged Commodities Rules, 2011</span>.
          </p>

          {/* Call to Actions */}
          <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => onNavigate('scan')}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 flex items-center gap-2 text-base transition-all hover:scale-105"
            >
              <ScanLine className="w-5 h-5" />
              <span>Start Packaging Scan</span>
              <ArrowRight className="w-5 h-5" />
            </button>

            <button
              onClick={() => onNavigate('dashboard')}
              className="px-8 py-4 bg-slate-800/90 hover:bg-slate-700/90 text-slate-200 font-bold rounded-xl border border-slate-600 flex items-center gap-2 text-base transition-all"
            >
              <span>View Enforcement Dashboard</span>
            </button>
          </div>
        </div>
      </section>

      {/* 2. Visual 5-Step Workflow */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-10">
          <h2 className="text-xs font-bold text-blue-600 uppercase tracking-widest mb-1">
            End-to-End Pipeline
          </h2>
          <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-['Outfit']">
            How PRAMAN AI Evaluates Packaged Commodities
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[
            { step: '01', title: 'SCAN / UPLOAD', desc: 'Capture or upload pre-packaged commodity image with zero quality degradation.', icon: ScanLine, color: 'text-blue-600' },
            { step: '02', title: 'PREPROCESS & OCR', desc: 'OpenCV contrast enhancement & Tesseract 5.4 bounding box extraction.', icon: Layers, color: 'text-indigo-600' },
            { step: '03', title: 'DECLARATION PARSING', desc: 'Deterministic NLP extraction of MRP, Net Qty, Dates, Mfr & Helpline.', icon: Search, color: 'text-amber-600' },
            { step: '04', title: 'PCR RULE ENGINE', desc: 'Evaluate 12 statutory rule groups derived directly from 40 official gazettes.', icon: BookOpenCheck, color: 'text-emerald-600' },
            { step: '05', title: 'REPORT & EVIDENCE', desc: 'Generate 0-100 score, annotated image overlays, and statutory PDF/DOCX notice.', icon: FileText, color: 'text-purple-600' }
          ].map((item, idx) => {
            const Icon = item.icon;
            return (
              <div key={idx} className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm relative group hover:shadow-md transition-all">
                <div className="text-[11px] font-mono font-bold text-slate-400 mb-2">STEP {item.step}</div>
                <div className={`w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center mb-3 ${item.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <h4 className="text-sm font-bold text-slate-900 mb-1 font-['Outfit']">{item.title}</h4>
                <p className="text-xs text-slate-500 leading-relaxed">{item.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* 3. Core Feature Cards */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-10">
          <h2 className="text-xs font-bold text-blue-600 uppercase tracking-widest mb-1">
            Statutory Capabilities
          </h2>
          <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-['Outfit']">
            Built for Real-World Legal Metrology Enforcement
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: 'Deterministic PCR 2011 Engine',
              desc: 'Strictly zero hallucination. Every rule check links directly to the specific gazette and section in the 40 indexed dataset PDFs.',
              icon: BookOpenCheck,
              accent: 'border-l-4 border-l-blue-600'
            },
            {
              title: 'Visual Evidence & Bounding Boxes',
              desc: 'Identifies exactly WHERE each declaration is located on the package and overlays color-coded bounding boxes for instant inspector proof.',
              icon: Layers,
              accent: 'border-l-4 border-l-amber-500'
            },
            {
              title: 'Explainable Compliance Scoring',
              desc: 'Transparent 0-100 score weighted across Declaration Completeness, Metric Units, Pricing & USP Consistency, and Grievance Redressal.',
              icon: Award,
              accent: 'border-l-4 border-l-emerald-600'
            },
            {
              title: 'Official PDF & Word Reports',
              desc: 'One-click generation of statutory inspection notices with Government of India branding, complete evidence tables, and inspector sign-off.',
              icon: FileText,
              accent: 'border-l-4 border-l-purple-600'
            },
            {
              title: 'Senior-Friendly Accessibility',
              desc: 'High-contrast themes, large typography mode, and text-to-speech voice guidance designed for elderly or field enforcement personnel.',
              icon: Users,
              accent: 'border-l-4 border-l-teal-600'
            },
            {
              title: 'Audit Trail & Product Catalog',
              desc: 'Immutable log of every scan, review, and supervisor override with repeat-offender tracking across manufacturers.',
              icon: Database,
              accent: 'border-l-4 border-l-rose-600'
            }
          ].map((card, idx) => {
            const Icon = card.icon;
            return (
              <div key={idx} className={`bg-white p-6 rounded-2xl border border-slate-200 shadow-sm ${card.accent}`}>
                <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center text-slate-800 mb-3">
                  <Icon className="w-5 h-5" />
                </div>
                <h4 className="text-base font-bold text-slate-900 mb-2 font-['Outfit']">{card.title}</h4>
                <p className="text-xs text-slate-600 leading-relaxed">{card.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* 4. Instant 2-Minute Judge Demo Banner */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="bg-gradient-to-r from-slate-900 to-[#0F2942] text-white rounded-3xl p-8 sm:p-10 border border-slate-700 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
          <div className="space-y-2 text-center md:text-left">
            <div className="inline-flex items-center gap-1.5 bg-amber-500/20 text-amber-300 px-3 py-1 rounded-full text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>SIH 2026 Demonstration Mode</span>
            </div>
            <h3 className="text-2xl font-bold font-['Outfit']">Ready to test PRAMAN AI right now?</h3>
            <p className="text-sm text-slate-300 max-w-xl">
              Launch our pre-loaded test packages (Compliant Atta, Non-Compliant Sunflower Oil, or Critical Violation Snack) to evaluate the pipeline in seconds.
            </p>
          </div>
          <button
            onClick={() => onNavigate('scan')}
            className="shrink-0 px-6 py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded-xl shadow-lg flex items-center gap-2 transition-all hover:scale-105 text-sm"
          >
            <span>Launch Live Scan Studio</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </section>
    </div>
  );
};
