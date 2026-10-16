import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Terminal, 
  Search, 
  RotateCcw, 
  FileCode, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  Layers, 
  BookOpen, 
  Loader2 
} from 'lucide-react';

import Navbar from './components/Navbar';
import SecurityDisclaimer from './components/SecurityDisclaimer';
import SampleCodeSelector from './components/SampleCodeSelector';
import FileUploader from './components/FileUploader';
import SeveritySummary from './components/SeveritySummary';
import FindingCard from './components/FindingCard';
import EmptyResultState from './components/EmptyResultState';
import ErrorAlert from './components/ErrorAlert';

import { fetchHealth, fetchSampleCodes, analyzeSourceFile } from './utils/api';

export default function App() {
  const [health, setHealth] = useState(null);
  const [samples, setSamples] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // Initial load: check health and retrieve educational sample codes
  useEffect(() => {
    loadHealth();
    loadSamples();
  }, []);

  const loadHealth = async () => {
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (err) {
      console.error('Failed to load health:', err);
    }
  };

  const loadSamples = async () => {
    try {
      const data = await fetchSampleCodes();
      setSamples(data);
    } catch (err) {
      console.error('Failed to load sample codes:', err);
    }
  };

  // Handle local file selection
  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setError(null);
    setAnalysisResult(null);

    // Read text content for preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setFileContent(e.target.result || '');
    };
    reader.onerror = () => {
      setFileContent('(Could not read text preview)');
    };
    reader.readAsText(file);
  };

  // Handle educational sample selection (create virtual File)
  const handleSelectSample = (sample) => {
    const blob = new Blob([sample.code], { type: 'text/plain' });
    const virtualFile = new File([blob], sample.filename, {
      type: sample.language === 'python' ? 'text/x-python' : 'text/javascript',
      lastModified: Date.now()
    });

    setSelectedFile(virtualFile);
    setFileContent(sample.code);
    setError(null);
    setAnalysisResult(null);
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setFileContent('');
    setAnalysisResult(null);
    setError(null);
    setSeverityFilter('ALL');
    setSearchQuery('');
  };

  // Execute Review Project analysis
  const handleReviewProject = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await analyzeSourceFile(selectedFile);
      setAnalysisResult(result);
      setSeverityFilter('ALL');
      setSearchQuery('');
    } catch (err) {
      console.error('Analysis failed:', err);
      setError(err.message || 'An error occurred during static analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Filter findings based on active severity filter and search term
  const filteredFindings = (analysisResult?.findings || []).filter((f) => {
    // 1. Severity filter
    if (severityFilter !== 'ALL' && f.severity !== severityFilter) {
      return false;
    }

    // 2. Search query filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      const matchRule = f.rule_id?.toLowerCase().includes(query);
      const matchTitle = f.title?.toLowerCase().includes(query);
      const matchDesc = f.description?.toLowerCase().includes(query);
      const matchSnippet = f.code_snippet?.toLowerCase().includes(query);
      return matchRule || matchTitle || matchDesc || matchSnippet;
    }

    return true;
  });

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      {/* Top Navigation */}
      <Navbar health={health} onRefreshHealth={loadHealth} />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Hero Section */}
        <div className="text-center space-y-3 pt-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold">
            <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
            <span>AI-Assisted Source-Code Review for Students</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white">
            Inspect Code. Learn Risks. <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">Ship Securely.</span>
          </h1>

          <p className="max-w-2xl mx-auto text-sm sm:text-base text-slate-400 leading-relaxed">
            Upload your Python or JavaScript project file. ProjectLens AI runs verified static-analysis engines (Bandit &amp; ESLint) in an isolated environment, translating raw diagnostics into student-friendly risk breakdowns and actionable fixes.
          </p>
        </div>

        {/* Security Disclaimer Banner */}
        <SecurityDisclaimer />

        {/* Educational Sample Code Quick-Loaders */}
        <SampleCodeSelector
          samples={samples}
          onSelectSample={handleSelectSample}
          isAnalyzing={isAnalyzing}
        />

        {/* File Upload & Review Trigger */}
        <FileUploader
          selectedFile={selectedFile}
          fileContent={fileContent}
          onFileSelect={handleFileSelect}
          onClearFile={handleClearFile}
          onReviewProject={handleReviewProject}
          isAnalyzing={isAnalyzing}
        />

        {/* Error State */}
        {error && (
          <ErrorAlert
            message={error}
            onRetry={handleReviewProject}
            onDismiss={() => setError(null)}
          />
        )}

        {/* Loading State Overlay */}
        {isAnalyzing && (
          <div className="rounded-2xl border border-indigo-500/30 bg-slate-900/90 p-8 sm:p-12 text-center space-y-4 shadow-2xl relative overflow-hidden">
            <div className="w-16 h-16 rounded-2xl bg-indigo-500/15 border border-indigo-500/30 text-indigo-400 mx-auto flex items-center justify-center animate-pulse">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
            <div className="space-y-1.5">
              <h3 className="text-lg font-bold text-white">
                Performing Static Code Analysis
              </h3>
              <p className="text-xs sm:text-sm text-slate-400 max-w-md mx-auto">
                Validating syntax, inspecting AST patterns, and comparing against security rules in a sandboxed subprocess...
              </p>
            </div>
            <div className="flex items-center justify-center space-x-3 text-xs text-indigo-300 font-mono pt-2">
              <span className="w-2 h-2 rounded-full bg-indigo-400 animate-ping"></span>
              <span>Subprocess execution active &bull; Timeout: 25s</span>
            </div>
          </div>
        )}

        {/* Analysis Results View */}
        {analysisResult && (
          <div className="space-y-6 animate-in fade-in duration-300">
            
            {/* Results Header Card */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/90 p-5 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center space-x-2.5">
                  <h3 className="text-lg font-bold text-white font-mono">
                    {analysisResult.file_name}
                  </h3>
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${
                    analysisResult.file_type === 'python'
                      ? 'bg-blue-500/20 text-blue-300 border-blue-500/40'
                      : 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40'
                  }`}>
                    {analysisResult.file_type}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
                  <span className="flex items-center space-x-1">
                    <Layers className="w-3.5 h-3.5 text-slate-500" />
                    <span>Engine: <strong className="text-slate-200 font-medium">{analysisResult.tool_used}</strong></span>
                  </span>
                  <span>&bull;</span>
                  <span className="flex items-center space-x-1">
                    <Clock className="w-3.5 h-3.5 text-slate-500" />
                    <span>{new Date(analysisResult.scan_timestamp).toLocaleTimeString()}</span>
                  </span>
                  <span>&bull;</span>
                  <span>Size: {(analysisResult.file_size_bytes / 1024).toFixed(1)} KB</span>
                </div>
              </div>

              <button
                type="button"
                onClick={handleReviewProject}
                className="px-3.5 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-750 text-xs font-semibold text-slate-200 hover:text-white transition-colors flex items-center space-x-1.5 cursor-pointer shrink-0"
              >
                <RotateCcw className="w-3.5 h-3.5 text-indigo-400" />
                <span>Re-scan File</span>
              </button>
            </div>

            {/* Severity Summary & Filtering Pills */}
            <SeveritySummary
              summary={analysisResult.summary}
              currentFilter={severityFilter}
              onFilterChange={setSeverityFilter}
            />

            {/* If zero issues detected */}
            {analysisResult.summary?.total_issues === 0 ? (
              <EmptyResultState
                fileName={analysisResult.file_name}
                toolUsed={analysisResult.tool_used}
              />
            ) : (
              /* Findings List Section */
              <div className="space-y-4">
                
                {/* Findings Header & Search Bar */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pt-2">
                  <div className="flex items-center space-x-2">
                    <h3 className="text-base font-bold text-white">
                      Diagnostic Findings
                    </h3>
                    <span className="text-xs text-slate-400 font-mono">
                      ({filteredFindings.length} of {analysisResult.findings.length} displayed)
                    </span>
                  </div>

                  {/* Search / Filter input */}
                  <div className="relative w-full sm:w-64">
                    <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search rule or keyword..."
                      className="w-full bg-slate-900 border border-slate-750 rounded-xl pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                {/* Filtered Findings Cards */}
                {filteredFindings.length > 0 ? (
                  <div className="space-y-4">
                    {filteredFindings.map((finding, idx) => (
                      <FindingCard
                        key={finding.id || idx}
                        finding={finding}
                        index={idx}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="p-8 rounded-2xl border border-slate-800 bg-slate-900/50 text-center text-xs text-slate-400">
                    No findings match the selected filter ({severityFilter}) or search term.
                  </div>
                )}
              </div>
            )}

          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-8 mt-12 text-center text-xs text-slate-400">
        <div className="max-w-6xl mx-auto px-4 space-y-2">
          <div className="flex flex-wrap items-center justify-center gap-3 text-slate-400">
            <span>ProjectLens AI &bull; Built with FastAPI + React + Bandit + ESLint</span>
            <span>&bull;</span>
            <span className="text-amber-400/80">Static analysis only &bull; Zero code execution</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Designed for computer science students and educators to study secure coding principles.
          </p>
        </div>
      </footer>
    </div>
  );
}
