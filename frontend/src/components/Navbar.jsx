import React, { useState } from 'react';
import { ShieldCheck, Activity, Terminal, AlertCircle, Info, ChevronDown } from 'lucide-react';

export default function Navbar({ health, onRefreshHealth }) {
  const [showStatusDetails, setShowStatusDetails] = useState(false);

  const isHealthy = health?.status === 'healthy';
  const isOffline = health?.status === 'offline';

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand / Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-bold tracking-tight text-white">ProjectLens</span>
              <span className="text-xs font-semibold px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">AI</span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">AI-Assisted Student Code Review Platform</p>
          </div>
        </div>

        {/* Center Tech Stack Indicator */}
        <div className="hidden md:flex items-center space-x-4 text-xs text-slate-400">
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-800/80 border border-slate-700/60">
            <span className="w-2 h-2 rounded-full bg-blue-400"></span>
            <span>Python (Bandit)</span>
          </div>
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-800/80 border border-slate-700/60">
            <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
            <span>JavaScript (ESLint)</span>
          </div>
        </div>

        {/* Backend Engine Status Pill */}
        <div className="relative">
          <button
            onClick={() => setShowStatusDetails(!showStatusDetails)}
            className={`flex items-center space-x-2 text-xs font-medium px-3 py-1.5 rounded-full border transition-all ${
              isHealthy
                ? 'bg-emerald-950/40 text-emerald-300 border-emerald-500/40 hover:bg-emerald-900/40'
                : isOffline
                ? 'bg-rose-950/40 text-rose-300 border-rose-500/40 hover:bg-rose-900/40'
                : 'bg-amber-950/40 text-amber-300 border-amber-500/40 hover:bg-amber-900/40'
            }`}
            title="Click to view static engine status"
          >
            <span className={`w-2 h-2 rounded-full ${
              isHealthy ? 'bg-emerald-400 animate-pulse' : isOffline ? 'bg-rose-500' : 'bg-amber-400'
            }`}></span>
            <span>{isHealthy ? 'Engines Online' : isOffline ? 'Backend Offline' : 'Degraded Engines'}</span>
            <ChevronDown className="w-3.5 h-3.5 opacity-60" />
          </button>

          {/* Engine Status Popover */}
          {showStatusDetails && (
            <div className="absolute right-0 mt-2 w-80 rounded-xl bg-slate-900 border border-slate-700 p-4 shadow-2xl z-50 text-left">
              <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800">
                <span className="text-xs font-semibold text-slate-300">Static Analysis Engines</span>
                <button
                  onClick={onRefreshHealth}
                  className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
                >
                  <Activity className="w-3 h-3" />
                  <span>Refresh</span>
                </button>
              </div>

              <div className="space-y-2.5 text-xs">
                {/* Bandit Status */}
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-medium text-slate-200">Bandit (Python)</p>
                    <p className="text-[11px] text-slate-400">
                      {health?.tools?.bandit?.version_or_path || (health?.tools?.bandit?.available ? 'Available' : health?.tools?.bandit?.error || 'Unavailable')}
                    </p>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                    health?.tools?.bandit?.available ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                  }`}>
                    {health?.tools?.bandit?.available ? 'Ready' : 'Missing'}
                  </span>
                </div>

                {/* ESLint Status */}
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-medium text-slate-200">ESLint (JavaScript)</p>
                    <p className="text-[11px] text-slate-400">
                      {health?.tools?.eslint?.version_or_path || (health?.tools?.eslint?.available ? 'Available' : health?.tools?.eslint?.error || 'Unavailable')}
                    </p>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                    health?.tools?.eslint?.available ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                  }`}>
                    {health?.tools?.eslint?.available ? 'Ready' : 'Missing'}
                  </span>
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] text-slate-400 flex items-center space-x-1">
                <Info className="w-3 h-3 text-slate-400 shrink-0" />
                <span>Backend runs controlled subprocesses without execution.</span>
              </div>
            </div>
          )}
        </div>

      </div>
    </header>
  );
}
