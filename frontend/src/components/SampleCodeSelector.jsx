import React from 'react';
import { Sparkles, FileCode, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function SampleCodeSelector({ samples, onSelectSample, isAnalyzing }) {
  if (!samples || samples.length === 0) return null;

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 sm:p-5 text-left">
      <div className="flex items-center space-x-2 mb-3">
        <Sparkles className="w-4 h-4 text-indigo-400" />
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
          Try Pre-Configured Student Samples
        </h3>
        <span className="text-[10px] text-slate-500 hidden sm:inline">— Test with 1 click</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {samples.map((sample) => {
          const isVulnerable = sample.id.includes('vulnerable');
          const isPython = sample.language === 'python';

          return (
            <button
              key={sample.id}
              disabled={isAnalyzing}
              onClick={() => onSelectSample(sample)}
              className="group p-3 rounded-xl border border-slate-800 bg-slate-900/90 hover:bg-slate-850 hover:border-indigo-500/50 transition-all text-left flex flex-col justify-between hover:shadow-lg hover:shadow-indigo-500/10 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                    isPython 
                      ? 'bg-blue-500/15 text-blue-300 border-blue-500/30'
                      : 'bg-yellow-500/15 text-yellow-300 border-yellow-500/30'
                  }`}>
                    {isPython ? 'Python' : 'JavaScript'}
                  </span>

                  <span className={`text-[10px] flex items-center space-x-1 ${
                    isVulnerable ? 'text-amber-400' : 'text-emerald-400'
                  }`}>
                    {isVulnerable ? (
                      <>
                        <AlertTriangle className="w-3 h-3" />
                        <span>Flaws</span>
                      </>
                    ) : (
                      <>
                        <CheckCircle2 className="w-3 h-3" />
                        <span>Clean</span>
                      </>
                    )}
                  </span>
                </div>

                <h4 className="text-xs font-semibold text-slate-200 group-hover:text-indigo-300 transition-colors line-clamp-1">
                  {sample.title}
                </h4>
                <p className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                  {sample.description}
                </p>
              </div>

              <div className="mt-2.5 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400">
                <span className="font-mono text-slate-400">{sample.filename}</span>
                <span className="text-indigo-400 group-hover:underline">Load &rarr;</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
