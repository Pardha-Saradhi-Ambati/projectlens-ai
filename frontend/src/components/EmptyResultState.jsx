import React from 'react';
import { ShieldCheck, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

export default function EmptyResultState({ fileName, toolUsed }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 p-8 sm:p-12 text-center space-y-6 shadow-2xl relative overflow-hidden">
      <div className="w-20 h-20 rounded-3xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 mx-auto flex items-center justify-center shadow-lg shadow-emerald-500/10">
        <CheckCircle2 className="w-10 h-10" />
      </div>

      <div className="max-w-md mx-auto space-y-2">
        <span className="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
          Scan Completed &bull; Zero Issues Found
        </span>
        <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight pt-2">
          No Heuristic Findings Detected
        </h3>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          The <span className="font-mono text-indigo-300">{toolUsed}</span> static engine reviewed{' '}
          <span className="font-mono text-white font-medium">{fileName}</span> and did not trigger any configured AST risk rules or lint errors.
        </p>
      </div>

      {/* Critical Security Clarification Box */}
      <div className="max-w-lg mx-auto p-4 rounded-2xl bg-amber-500/10 border border-amber-500/25 text-left text-xs text-amber-200/90 space-y-1.5">
        <div className="flex items-center space-x-2 font-semibold text-amber-300">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
          <span>Notice: Clean Static Scan &ne; Complete Security Guarantee</span>
        </div>
        <p className="leading-relaxed text-slate-300 pl-6">
          Static analysis only checks known syntax and library patterns. A file with 0 findings can still have
          business logic defects, runtime vulnerabilities, unhandled exception branches, or improper authentication flows.
        </p>
      </div>
    </div>
  );
}
