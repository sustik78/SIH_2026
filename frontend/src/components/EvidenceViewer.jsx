import React, { useState } from 'react';
import { 
  Eye, 
  Layers, 
  AlertCircle, 
  CheckCircle2, 
  ZoomIn, 
  Maximize2, 
  FileText,
  HelpCircle,
  ExternalLink
} from 'lucide-react';

export const EvidenceViewer = ({ 
  originalImageUrl, 
  annotatedImageUrl, 
  evidenceItems = [], 
  results = [] 
}) => {
  const [viewMode, setViewMode] = useState('annotated'); // 'annotated', 'original', 'split'
  const [selectedItem, setSelectedItem] = useState(null);

  const activeImage = viewMode === 'annotated' && annotatedImageUrl ? annotatedImageUrl : originalImageUrl;

  const violationItems = results.filter(r => r.status === 'VIOLATION' || r.status === 'WARNING');

  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden flex flex-col">
      {/* Viewer Controls Header */}
      <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-blue-700" />
          <h3 className="text-sm font-bold text-slate-800 tracking-tight">
            Visual Packaging Evidence & Annotation Layer
          </h3>
        </div>

        {/* View Mode Toggle Buttons */}
        <div className="flex items-center bg-slate-200/80 p-1 rounded-lg text-xs font-semibold text-slate-700">
          <button
            onClick={() => setViewMode('annotated')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              viewMode === 'annotated' ? 'bg-white text-blue-800 shadow-sm font-bold' : 'hover:text-slate-900'
            }`}
          >
            AI Bounding Boxes Overlay
          </button>
          <button
            onClick={() => setViewMode('original')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              viewMode === 'original' ? 'bg-white text-blue-800 shadow-sm font-bold' : 'hover:text-slate-900'
            }`}
          >
            Raw Package Image
          </button>
        </div>
      </div>

      {/* Main Evidence Visual Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-0 min-h-[460px]">
        {/* Left / Center: Interactive Image Canvas */}
        <div className="lg:col-span-7 p-4 bg-slate-950 flex flex-col items-center justify-center relative overflow-hidden border-b lg:border-b-0 lg:border-r border-slate-800">
          {activeImage ? (
            <div className="relative group max-h-[500px] flex items-center justify-center">
              <img
                src={activeImage}
                alt="Product Packaging Evidence"
                className="max-h-[480px] w-auto object-contain rounded-lg shadow-2xl border border-slate-800"
              />
              <div className="absolute top-3 left-3 bg-black/75 backdrop-blur-sm text-white px-2.5 py-1 rounded text-[11px] font-mono border border-white/10 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>{viewMode === 'annotated' ? 'AI ANNOTATED EVIDENCE' : 'ORIGINAL CAPTURE'}</span>
              </div>
            </div>
          ) : (
            <div className="text-slate-500 text-sm flex flex-col items-center gap-2">
              <AlertCircle className="w-8 h-8 text-slate-600" />
              <span>No image stream available</span>
            </div>
          )}
        </div>

        {/* Right: Cropped Evidence Cards & Rule Explanations */}
        <div className="lg:col-span-5 p-4 flex flex-col justify-between bg-slate-50/50 max-h-[520px] overflow-y-auto">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4 text-amber-600" />
                <span>Detected Infraction Crops ({violationItems.length})</span>
              </h4>
              <span className="text-[11px] text-slate-500">Legal Metrology Act, 2009</span>
            </div>

            {violationItems.length === 0 ? (
              <div className="p-6 bg-emerald-50 border border-emerald-200 rounded-xl text-center">
                <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
                <h5 className="text-sm font-bold text-emerald-900">Zero Rule Violations</h5>
                <p className="text-xs text-emerald-700 mt-1">
                  All mandatory packaging declarations are present and compliant with PCR 2011 specifications.
                </p>
              </div>
            ) : (
              <div className="space-y-2.5">
                {violationItems.map((item, idx) => {
                  const isViolation = item.status === 'VIOLATION';
                  const isSelected = selectedItem?.rule_id === item.rule_id;
                  return (
                    <div
                      key={idx}
                      onClick={() => setSelectedItem(item)}
                      className={`p-3 rounded-xl border transition-all cursor-pointer ${
                        isSelected 
                          ? 'border-blue-600 bg-blue-50/80 shadow-md ring-1 ring-blue-500' 
                          : isViolation 
                            ? 'border-rose-200 bg-rose-50/50 hover:bg-rose-50' 
                            : 'border-amber-200 bg-amber-50/50 hover:bg-amber-50'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2 mb-1.5">
                        <div className="flex items-center gap-1.5">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                            isViolation ? 'bg-rose-600 text-white' : 'bg-amber-600 text-white'
                          }`}>
                            {item.status}
                          </span>
                          <span className="text-xs font-bold text-slate-900 font-mono">
                            {item.rule_id}
                          </span>
                        </div>
                        <span className="text-[10px] text-slate-500 font-semibold">
                          Severity: {item.severity}
                        </span>
                      </div>

                      <h5 className="text-xs font-semibold text-slate-900 mb-1">
                        {item.rule_name}
                      </h5>

                      <p className="text-[11px] text-slate-700 leading-relaxed mb-2">
                        {item.explanation}
                      </p>

                      <div className="bg-white/80 p-2 rounded border border-slate-200/80 text-[10px] text-slate-600">
                        <span className="font-semibold text-slate-900">Legal Source: </span>
                        <span>{item.source_section}</span>
                        <span className="text-slate-400 block truncate font-mono text-[9px] mt-0.5">{item.source_document}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-200 text-[11px] text-slate-700 flex items-center justify-between">
            <span className="flex items-center gap-1">
              <HelpCircle className="w-3.5 h-3.5 text-slate-700" />
              <span>Evidence crops are preserved in audit trail</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
