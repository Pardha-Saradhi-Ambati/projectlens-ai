import React, { useState } from 'react';
import { 
  AlertOctagon, 
  AlertTriangle, 
  Info, 
  ExternalLink, 
  ChevronDown, 
  ChevronUp, 
  Lightbulb, 
  ShieldAlert, 
  CheckCircle, 
  Copy, 
  Check 
} from 'lucide-react';

export default function FindingCard({ finding, index }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [copied, setCopied] = useState(false);

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'HIGH':
        return {
          bg: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
          dot: 'bg-rose-500',
          icon: AlertOctagon,
          label: 'High Severity'
        };
      case 'MEDIUM':
        return {
          bg: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
          dot: 'bg-amber-500',
          icon: AlertTriangle,
          label: 'Medium Severity'
        };
      case 'LOW':
        return {
          bg: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
          dot: 'bg-blue-400',
          icon: Info,
          label: 'Low Severity'
        };
      default:
        return {
          bg: 'bg-slate-700/50 text-slate-300 border-slate-600',
          dot: 'bg-slate-400',
          icon: Info,
          label: 'Info'
        };
    }
  };

  const badge = getSeverityBadge(finding.severity);
  const Icon = badge.icon;

  const handleCopyCode = (text) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/90 shadow-xl overflow-hidden transition-all hover:border-slate-750 text-left">
      {/* Finding Header */}
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-4 sm:p-5 flex items-start justify-between gap-4 cursor-pointer hover:bg-slate-850/60 transition-colors"
      >
        <div className="flex items-start space-x-3.5">
          <div className={`p-2 rounded-xl border ${badge.bg} shrink-0 mt-0.5`}>
            <Icon className="w-5 h-5" />
          </div>

          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${badge.bg}`}>
                {badge.label}
              </span>

              <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700">
                {finding.rule_id}
              </span>

              {finding.line_number && (
                <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  Line {finding.line_number}{finding.column_number ? `:${finding.column_number}` : ''}
                </span>
              )}
            </div>

            <h4 className="text-sm sm:text-base font-semibold text-white pt-1">
              {finding.title || finding.description}
            </h4>

            <p className="text-xs text-slate-300 leading-relaxed">
              {finding.description}
            </p>
          </div>
        </div>

        <button 
          type="button"
          className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 shrink-0"
          aria-label={isExpanded ? 'Collapse finding' : 'Expand finding'}
        >
          {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
      </div>

      {/* Expanded Educational Guidance Section */}
      {isExpanded && (
        <div className="border-t border-slate-800/80 bg-slate-950/40 p-4 sm:p-5 space-y-4">
          
          {/* Flagged Code Snippet */}
          {finding.code_snippet && (
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span className="font-semibold uppercase tracking-wider text-slate-400">Flagged Code Location</span>
                {finding.line_number && <span>Line {finding.line_number}</span>}
              </div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/90 font-mono text-xs text-rose-300/90 overflow-x-auto whitespace-pre-wrap">
                {finding.code_snippet}
              </div>
            </div>
          )}

          {/* Educational Risk Explanation */}
          {finding.risk_explanation && (
            <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5">
              <div className="flex items-center space-x-1.5 text-xs font-semibold text-amber-300">
                <ShieldAlert className="w-4 h-4 text-amber-400" />
                <span>Why This Matters (Risk Breakdown for Students)</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed pl-5.5">
                {finding.risk_explanation}
              </p>
            </div>
          )}

          {/* Recommendation */}
          {finding.recommendation && (
            <div className="p-3.5 rounded-xl bg-indigo-950/20 border border-indigo-500/20 space-y-1.5">
              <div className="flex items-center space-x-1.5 text-xs font-semibold text-indigo-300">
                <Lightbulb className="w-4 h-4 text-indigo-400" />
                <span>Recommendation for Improvement</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed pl-5.5">
                {finding.recommendation}
              </p>
            </div>
          )}

          {/* Code Fix Example */}
          {finding.code_fix_example && (
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span className="font-semibold uppercase tracking-wider text-emerald-400 flex items-center space-x-1">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Recommended Fix Pattern</span>
                </span>
                <button
                  type="button"
                  onClick={() => handleCopyCode(finding.code_fix_example)}
                  className="flex items-center space-x-1 text-[11px] text-slate-400 hover:text-white px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 transition-colors cursor-pointer"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
              </div>

              <pre className="p-3 rounded-xl bg-slate-950 border border-emerald-500/20 font-mono text-xs text-emerald-300/90 overflow-x-auto whitespace-pre leading-relaxed">
                {finding.code_fix_example}
              </pre>
            </div>
          )}

          {/* External Reference Link */}
          {finding.reference_url && (
            <div className="pt-1 flex items-center justify-end">
              <a
                href={finding.reference_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[11px] text-indigo-400 hover:text-indigo-300 flex items-center space-x-1 hover:underline"
              >
                <span>Rule Documentation</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          )}

        </div>
      )}
    </div>
  );
}
