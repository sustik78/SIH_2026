import React from 'react';
import { ShieldCheck, AlertTriangle, XCircle, CheckCircle2 } from 'lucide-react';

export const ScoreGauge = ({ score = 0, status = "PENDING", size = 150 }) => {
  const radius = 58;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = "#059669"; // Green
  let badgeBg = "bg-emerald-50 text-emerald-800 border-emerald-300";
  let statusIcon = CheckCircle2;

  if (status === "NON-COMPLIANT" || score < 70) {
    color = "#DC2626"; // Red
    badgeBg = "bg-rose-50 text-rose-800 border-rose-300";
    statusIcon = XCircle;
  } else if (status === "PENDING REVIEW" || (score >= 70 && score < 85)) {
    color = "#D97706"; // Amber
    badgeBg = "bg-amber-50 text-amber-800 border-amber-300";
    statusIcon = AlertTriangle;
  }

  const Icon = statusIcon;

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} viewBox="0 0 140 140" className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke="#E2E8F0"
            strokeWidth="10"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke={color}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center content */}
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold tracking-tight text-slate-900 font-['Outfit']">
            {score}
          </span>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
            Out of 100
          </span>
        </div>
      </div>

      {/* Compliance Decision Badge */}
      <div className="mt-3 flex items-center gap-1.5">
        <span className={`px-3 py-1 rounded-full text-xs font-bold border flex items-center gap-1.5 uppercase tracking-wider ${badgeBg}`}>
          <Icon className="w-4 h-4 shrink-0" />
          <span>{status}</span>
        </span>
      </div>
    </div>
  );
};
