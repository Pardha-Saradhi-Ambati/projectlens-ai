import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function SecurityDisclaimer({ variant = 'banner' }) {
  if (variant === 'compact') {
    return (
      <div className="flex items-center space-x-2 text-xs text-amber-300/80 bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-lg">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
        <span>Heuristic findings highlight potential risks and do not guarantee total application security.</span>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-r from-amber-950/20 via-slate-900 to-slate-900 p-4 sm:p-5 relative overflow-hidden shadow-lg">
      <div className="absolute top-0 right-0 -mr-6 -mt-6 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl pointer-events-none"></div>
      
      <div className="flex items-start space-x-3.5">
        <div className="p-2 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-400 shrink-0 mt-0.5">
          <ShieldAlert className="w-5 h-5" />
        </div>
        
        <div className="space-y-1.5 text-left">
          <div className="flex items-center space-x-2">
            <h4 className="text-sm font-semibold text-amber-200 tracking-wide">
              Security Guarantee Disclaimer & Educational Notice
            </h4>
            <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-amber-400/15 text-amber-300 border border-amber-400/30">
              Important
            </span>
          </div>
          
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            ProjectLens AI uses automated static analysis (AST inspection and heuristic rules via Bandit &amp; ESLint). 
            Findings represent <strong>potential risks, anti-patterns, or policy violations</strong>, not certified vulnerabilities.
          </p>

          <p className="text-xs text-amber-300/90 leading-relaxed font-medium">
            ⚠️ <strong>Crucial rule:</strong> Receiving 0 findings does <span className="underline decoration-amber-400/60 underline-offset-2">never</span> guarantee that your code is completely secure or free of logic flaws. Always combine automated scans with defensive input validation, least-privilege principles, and peer code reviews.
          </p>
        </div>
      </div>
    </div>
  );
}
