import React from 'react';
import { AlertCircle, RefreshCw, XCircle, Terminal } from 'lucide-react';

export default function ErrorAlert({ message, onRetry, onDismiss }) {
  if (!message) return null;

  return (
    <div className="rounded-2xl border border-rose-500/40 bg-gradient-to-r from-rose-950/40 via-slate-900 to-slate-900 p-5 shadow-2xl text-left">
      <div className="flex items-start space-x-3.5">
        <div className="p-2.5 rounded-xl bg-rose-500/20 border border-rose-500/40 text-rose-400 shrink-0 mt-0.5">
          <XCircle className="w-6 h-6" />
        </div>

        <div className="space-y-2 flex-1">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-rose-200 uppercase tracking-wide">
              Analysis Request Failed
            </h4>
            {onDismiss && (
              <button
                type="button"
                onClick={onDismiss}
                className="text-xs text-slate-400 hover:text-white px-2 py-0.5 rounded hover:bg-slate-800"
              >
                Dismiss
              </button>
            )}
          </div>

          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-mono bg-slate-950/60 p-3 rounded-lg border border-slate-800/80">
            {message}
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-1 text-xs text-slate-400">
            {onRetry && (
              <button
                type="button"
                onClick={onRetry}
                className="px-3.5 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 font-medium border border-rose-500/40 transition-colors flex items-center space-x-1.5 cursor-pointer"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Try Again</span>
              </button>
            )}

            <div className="flex items-center space-x-1 text-[11px] text-slate-400">
              <Terminal className="w-3.5 h-3.5" />
              <span>Ensure backend is running: <code className="text-indigo-300 font-mono">uvicorn app.main:app --reload</code></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
