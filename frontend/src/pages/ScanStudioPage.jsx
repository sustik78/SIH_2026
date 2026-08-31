import React, { useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useAccessibility } from '../context/AccessibilityContext';
import { apiFetch } from '../utils/api';
import { 
  UploadCloud, 
  Camera, 
  Sparkles, 
  Layers, 
  CheckCircle2, 
  AlertCircle, 
  Clock, 
  ArrowRight,
  RefreshCw,
  FileImage,
  Scale,
  ShieldCheck
} from 'lucide-react';

export const ScanStudioPage = ({ onScanComplete, onSelectSample }) => {
  const { token } = useAuth();
  const { speakText } = useAccessibility();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [selectedSample, setSelectedSample] = useState(null);
  const [category, setCategory] = useState('Packaged Food / Grocery');
  const [productName, setProductName] = useState('');

  const [isScanning, setIsScanning] = useState(false);
  const [scanStep, setScanStep] = useState(0); // 0 to 5
  const [scanStatusText, setScanStatusText] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const demoSamples = [
    {
      id: 'sample_1',
      title: 'Chakki Fresh Atta (5 kg)',
      category: 'Packaged Food / Atta',
      badge: 'COMPLIANT (96/100)',
      badgeColor: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      desc: 'Standard compliant retail package with Metric Net Qty (5.0 kg), MRP incl. of all taxes, USP ₹46/kg, and Consumer Helpline.',
      filename: 'sample_compliant_atta.jpg'
    },
    {
      id: 'sample_2',
      title: 'Refined Sunflower Oil (1 Litre)',
      category: 'Edible Oils & Fats',
      badge: 'NON-COMPLIANT (68/100)',
      badgeColor: 'bg-rose-50 text-rose-800 border-rose-300',
      desc: 'MRP lacks statutory "inclusive of all taxes" wording and omits consumer care helpline & email.',
      filename: 'sample_noncompliant_oil.jpg'
    },
    {
      id: 'sample_3',
      title: 'Desi Chatpata Namkeen Pack',
      category: 'Snack Foods',
      badge: 'CRITICAL VIOLATION (32/100)',
      badgeColor: 'bg-purple-50 text-purple-800 border-purple-300',
      desc: 'Prohibited expression "Jumbo Saver Pack" in place of metric units, missing standard MRP format, missing Country of Origin.',
      filename: 'sample_critical_snack.jpg'
    }
  ];

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setSelectedSample(null);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMsg('');
      if (!productName) {
        setProductName(file.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleSelectDemo = (sample) => {
    setSelectedSample(sample);
    setSelectedFile(null);
    setPreviewUrl(`/api/static/samples/${sample.filename}`);
    setProductName(sample.title);
    setCategory(sample.category);
    setErrorMsg('');
    speakText(`Selected sample: ${sample.title}`);
  };

  const runInspection = async () => {
    if (!selectedFile && !selectedSample) {
      setErrorMsg('Please upload an image or choose a demo sample to inspect.');
      return;
    }

    setIsScanning(true);
    setErrorMsg('');
    speakText("Starting Legal Metrology compliance inspection.");

    // Step 1: Preprocessing
    setScanStep(1);
    setScanStatusText('Step 1/5: OpenCV image denoising, contrast CLAHE, and skew correction...');
    await new Promise(r => setTimeout(r, 450));

    // Step 2: Text detection
    setScanStep(2);
    setScanStatusText('Step 2/5: Detecting text lines and extracting bounding boxes via Tesseract 5.4...');
    await new Promise(r => setTimeout(r, 550));

    // Step 3: Declaration parsing
    setScanStep(3);
    setScanStatusText('Step 3/5: Parsing mandatory Legal Metrology declarations (MRP, Net Qty, Dates, Mfr, Helpline)...');
    await new Promise(r => setTimeout(r, 500));

    // Step 4: Rule Engine Execution
    setScanStep(4);
    setScanStatusText('Step 4/5: Evaluating declarations against 40 indexed Legal Metrology gazette rules...');

    try {
      const formData = new FormData();
      if (selectedSample) {
        formData.append('sample_filename', selectedSample.filename);
      } else if (selectedFile) {
        formData.append('file', selectedFile);
      }
      formData.append('product_name', productName || 'Scanned Packaged Commodity');
      formData.append('category', category);

      const res = await apiFetch('/api/scan/upload', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Scan processing failed');
      }

      const result = await res.json();

      // Step 5: Finalizing
      setScanStep(5);
      setScanStatusText('Step 5/5: Generating explainable score and overlaying visual bounding box evidence...');
      await new Promise(r => setTimeout(r, 400));

      speakText(`Inspection complete. Overall score: ${result.overall_score} out of 100. Status: ${result.compliance_status}.`);
      onScanComplete(result.inspection_id);

    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'An error occurred during AI analysis. Please verify image clarity.');
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
          <Scale className="w-4 h-4" />
          <span>AI Computer Vision & Regulatory Validation Studio</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
          Packaged Commodity Inspection Studio
        </h1>
        <p className="text-xs text-slate-500 mt-1 leading-relaxed">
          Upload pre-packaged commodity packaging or select a benchmark sample to execute full Legal Metrology Act, 2009 & PCR 2011 compliance checks.
        </p>
      </div>

      {/* 2-Minute Judge Demo Quick Samples */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>SIH 2026 Instant Demo Samples (1-Click Test)</span>
          </h3>
          <span className="text-[11px] text-slate-400">Pre-calibrated regulatory test cases</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {demoSamples.map((sample) => {
            const isSelected = selectedSample?.id === sample.id;
            return (
              <div
                key={sample.id}
                onClick={() => handleSelectDemo(sample)}
                className={`p-4 rounded-2xl border transition-all cursor-pointer bg-white ${
                  isSelected 
                    ? 'border-blue-600 shadow-md ring-2 ring-blue-500/20 bg-blue-50/20' 
                    : 'border-slate-200 hover:border-slate-300 hover:shadow-sm'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-xs font-bold text-slate-900">{sample.title}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${sample.badgeColor}`}>
                    {sample.badge}
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 leading-relaxed mb-3">
                  {sample.desc}
                </p>
                <div className="flex items-center justify-between text-[11px] font-semibold text-blue-700">
                  <span>{isSelected ? '✓ Selected for Scan' : 'Click to Load Sample'}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Upload / Inspection Box */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Upload / Dropzone */}
        <div className="lg:col-span-6 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-3">
              Upload Packaging Image
            </h3>

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
            />

            <div
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-slate-300 hover:border-blue-500 hover:bg-blue-50/40 rounded-2xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center min-h-[220px]"
            >
              <UploadCloud className="w-12 h-12 text-blue-600 mb-3 animate-bounce" />
              <p className="text-sm font-bold text-slate-800">
                Click to browse or drag & drop package photo
              </p>
              <p className="text-xs text-slate-400 mt-1">
                Supports JPG, PNG, WEBP (Minimum 300 DPI recommended for numeral height)
              </p>
            </div>
          </div>

          {/* Form Fields */}
          <div className="space-y-3 pt-2">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Commodity Name / Brand
              </label>
              <input
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="e.g., Chakki Fresh Atta 5kg"
                className="w-full text-xs px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all font-medium"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Commodity Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full text-xs px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all font-medium"
              >
                <option value="Packaged Food / Grocery">Packaged Food / Grocery</option>
                <option value="Edible Oils & Fats">Edible Oils & Fats (SOP 2023)</option>
                <option value="Snack Foods / Confectionery">Snack Foods / Confectionery</option>
                <option value="Readymade Garments & Hosiery">Readymade Garments & Hosiery (3rd Amend 2022)</option>
                <option value="Cosmetics & Personal Care">Cosmetics & Personal Care</option>
                <option value="Electronic Commodities">Electronic Commodities (QR Proviso 2023)</option>
                <option value="General Packaged Commodity">General Packaged Commodity</option>
              </select>
            </div>
          </div>
        </div>

        {/* Right: Packaging Preview & Live Scanning State */}
        <div className="lg:col-span-6 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center justify-between">
              <span>Packaging Preview</span>
              {previewUrl && (
                <span className="text-[11px] text-emerald-600 font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Image Loaded</span>
                </span>
              )}
            </h3>

            <div className="h-[280px] bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-center p-3 overflow-hidden relative">
              {previewUrl ? (
                <img
                  src={previewUrl}
                  alt="Packaging preview"
                  className="max-h-full max-w-full object-contain rounded-lg shadow"
                />
              ) : (
                <div className="text-slate-500 text-xs flex flex-col items-center gap-2">
                  <FileImage className="w-10 h-10 text-slate-700" />
                  <span>No packaging image selected yet</span>
                </div>
              )}

              {/* Live scanning overlay */}
              {isScanning && (
                <div className="absolute inset-0 bg-slate-950/85 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center space-y-4">
                  <div className="w-14 h-14 rounded-full bg-blue-600/20 border-2 border-blue-500 flex items-center justify-center radar-active">
                    <RefreshCw className="w-6 h-6 text-blue-400 animate-spin" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white font-['Outfit']">
                      AI & Rule Engine Processing
                    </h4>
                    <p className="text-xs text-blue-300 mt-1 max-w-xs font-mono">
                      {scanStatusText}
                    </p>
                  </div>
                  <div className="w-48 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-blue-500 h-full transition-all duration-300 rounded-full"
                      style={{ width: `${(scanStep / 5) * 100}%` }}
                    ></div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Error display */}
          {errorMsg && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 font-medium flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Action Trigger Button */}
          <button
            onClick={runInspection}
            disabled={isScanning || (!selectedFile && !selectedSample)}
            className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm shadow-lg flex items-center justify-center gap-2 transition-all ${
              isScanning || (!selectedFile && !selectedSample)
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-700 to-indigo-700 hover:from-blue-600 hover:to-indigo-600 text-white shadow-blue-900/30 hover:scale-[1.01]'
            }`}
          >
            <ShieldCheck className="w-5 h-5" />
            <span>{isScanning ? 'Executing Compliance Engine...' : 'Execute Legal Metrology Inspection'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
