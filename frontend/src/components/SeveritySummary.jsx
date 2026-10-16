import React from 'react';
import { AlertOctagon, AlertTriangle, Info, CheckCircle2, Shield, Filter } from 'lucide-react';

export default function SeveritySummary({ summary, currentFilter, onFilterChange }) {
  if (!summary) return null;

  const { total_issues = 0, high = 0, medium = 0, low = 0, info = 0 } = summary;

  const cards = [
    {
      id: 'ALL',
      label: 'Total Findings',
      count: total_issues,
      icon: Shield,
      color: 'border-slate-700 bg-slate-900/80 text-white',
      badgeColor: 'bg-slate-800 text-slate-300',
      activeRing: 'ring-2 ring-indigo-500'
    },
    {
      id: 'HIGH',
      label: 'High Severity',
      count: high,
      icon: AlertOctagon,
      color: 'border-rose-500/30 bg-rose-950/20 text-rose-200',
      badgeColor: 'bg-rose-500/20 text-rose-400 border border-rose-500/40',
      activeRing: 'ring-2 ring-rose-500'
    },
    {
      id: 'MEDIUM',
      label: 'Medium Severity',
      count: medium,
      icon: AlertTriangle,
      color: 'border-amber-500/30 bg-amber-950/20 text-amber-200',
      badgeColor: 'bg-amber-500/20 text-amber-400 border border-amber-500/40',
      activeRing: 'ring-2 ring-amber-500'
    },
    {
      id: 'LOW',
      label: 'Low Severity',
      count: low,
      icon: Info,
      color: 'border-blue-500/30 bg-blue-950/20 text-blue-200',
      badgeColor: 'bg-blue-500/20 text-blue-400 border border-blue-500/40',
      activeRing: 'ring-2 ring-blue-500'
    }
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span className="font-semibold uppercase tracking-wider text-slate-300 flex items-center space-x-1.5">
          <Filter className="w-3.5 h-3.5" />
          <span>Findings Summary &amp; Filters</span>
        </span>
        <span>Click card to filter results</span>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {cards.map((card) => {
          const Icon = card.icon;
          const isSelected = currentFilter === card.id;

          return (
            <button
              key={card.id}
              onClick={() => onFilterChange(card.id)}
              className={`p-4 rounded-2xl border text-left transition-all cursor-pointer relative overflow-hidden group ${card.color} ${
                isSelected ? card.activeRing + ' shadow-lg' : 'hover:border-slate-600'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400 group-hover:text-slate-300">
                  {card.label}
                </span>
                <Icon className="w-4 h-4 opacity-75 group-hover:scale-110 transition-transform" />
              </div>

              <div className="mt-3 flex items-baseline justify-between">
                <span className="text-2xl sm:text-3xl font-extrabold tracking-tight font-mono">
                  {card.count}
                </span>

                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${card.badgeColor}`}>
                  {card.count === 0 ? 'Zero' : `${card.count} rule${card.count === 1 ? '' : 's'}`}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
