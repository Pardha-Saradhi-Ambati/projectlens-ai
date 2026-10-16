import React, { useRef, useState } from 'react';
import { UploadCloud, FileCode2, Check, X, Play, Code, Eye, EyeOff, Loader2 } from 'lucide-react';

export default function FileUploader({
  selectedFile,
  fileContent,
  onFileSelect,
  onClearFile,
  onReviewProject,
  isAnalyzing
}) {
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showCodePreview, setShowCodePreview] = useState(false);
  const [localError, setLocalError] = useState(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const validateAndProcessFile = (file) => {
    setLocalError(null);
    if (!file) return;

    const lowerName = file.name.toLowerCase();
    const isPy = lowerName.endsWith('.py');
    const isJs = lowerName.endsWith('.js');

    if (!isPy && !isJs) {
      setLocalError(`Invalid file format "${file.name}". Please upload a Python (.py) or JavaScript (.js) file.`);
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      setLocalError('File size exceeds the 2MB limit. Please upload a smaller source file.');
      return;
    }

    onFileSelect(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      validateAndProcessFile(file);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      validateAndProcessFile(file);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const getFileType = (fileName) => {
    if (fileName.toLowerCase().endsWith('.py')) return { label: 'Python Source', color: 'bg-blue-500/20 text-blue-300 border-blue-500/30' };
    if (fileName.toLowerCase().endsWith('.js')) return { label: 'JavaScript Source', color: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30' };
    return { label: 'Source File', color: 'bg-slate-700 text-slate-300 border-slate-600' };
  };

  return (
    <div className="space-y-4">
      {/* Upload Dropzone */}
      {!selectedFile ? (
        <div
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-3xl p-8 sm:p-12 text-center transition-all cursor-pointer relative overflow-hidden group ${
            isDragOver
              ? 'border-indigo-400 bg-indigo-500/10 scale-[1.01]'
              : 'border-slate-700/80 bg-slate-900/60 hover:bg-slate-900 hover:border-slate-600'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileInputChange}
            accept=".py,.js"
            className="hidden"
          />

          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-500/20 via-slate-800 to-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-110 group-hover:border-indigo-400 transition-all">
              <UploadCloud className="w-8 h-8" />
            </div>

            <div className="space-y-1">
              <h3 className="text-base sm:text-lg font-semibold text-slate-200">
                Drag and drop your source file here
              </h3>
              <p className="text-xs sm:text-sm text-slate-400">
                or <span className="text-indigo-400 underline decoration-indigo-400/40 font-medium">browse from your computer</span>
              </p>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-[11px] text-slate-400">
              <span className="px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700/60 font-mono text-slate-300">.py (Bandit)</span>
              <span className="px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700/60 font-mono text-slate-300">.js (ESLint)</span>
              <span className="text-slate-400">Max size: 2MB</span>
            </div>
          </div>
        </div>
      ) : (
        /* Selected File Card */
        <div className="rounded-2xl border border-slate-700 bg-slate-900/90 p-5 shadow-xl text-left">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
            <div className="flex items-center space-x-3.5">
              <div className="w-12 h-12 rounded-xl bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 shrink-0">
                <FileCode2 className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h4 className="text-base font-semibold text-white font-mono break-all">
                    {selectedFile.name}
                  </h4>
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${getFileType(selectedFile.name).color}`}>
                    {getFileType(selectedFile.name).label}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Size: {formatFileSize(selectedFile.size)} &bull; Ready for static review
                </p>
              </div>
            </div>

            {/* Actions for selected file */}
            <div className="flex items-center space-x-2 w-full sm:w-auto justify-end">
              {fileContent && (
                <button
                  type="button"
                  onClick={() => setShowCodePreview(!showCodePreview)}
                  className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-750 transition-colors flex items-center space-x-1.5 cursor-pointer"
                >
                  {showCodePreview ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  <span>{showCodePreview ? 'Hide Code' : 'Preview Code'}</span>
                </button>
              )}

              <button
                type="button"
                disabled={isAnalyzing}
                onClick={onClearFile}
                className="px-3 py-1.5 rounded-lg border border-slate-700 hover:border-rose-500/40 bg-slate-800 hover:bg-rose-950/30 text-xs font-medium text-slate-300 hover:text-rose-300 transition-colors flex items-center space-x-1.5 cursor-pointer disabled:opacity-50"
                title="Remove file"
              >
                <X className="w-3.5 h-3.5" />
                <span>Remove</span>
              </button>
            </div>
          </div>

          {/* Code Preview Drawer */}
          {showCodePreview && fileContent && (
            <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs overflow-x-auto max-h-64 scrollbar-thin">
              <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800/80 text-[11px] text-slate-500">
                <span>Source Preview ({selectedFile.name})</span>
                <span>Read-only</span>
              </div>
              <pre className="text-slate-300 leading-relaxed whitespace-pre font-mono">
                {fileContent}
              </pre>
            </div>
          )}

          {/* Big Action: Review Project Button */}
          <div className="mt-5 flex flex-col sm:flex-row items-center justify-between gap-3 pt-3">
            <div className="text-xs text-slate-400 flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
              <span>Isolated subprocess engine &bull; Zero code execution</span>
            </div>

            <button
              type="button"
              id="review-project-button"
              disabled={isAnalyzing}
              onClick={onReviewProject}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-500 via-indigo-600 to-indigo-700 hover:from-indigo-400 hover:via-indigo-500 hover:to-indigo-600 text-white font-semibold text-sm shadow-lg shadow-indigo-500/25 transition-all flex items-center justify-center space-x-2 cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed group active:scale-[0.98]"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-white" />
                  <span>Analyzing AST &amp; Security Rules...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-white group-hover:scale-110 transition-transform" />
                  <span>Review Project</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Local validation error if any */}
      {localError && (
        <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs text-left flex items-start space-x-2">
          <X className="w-4 h-4 shrink-0 text-rose-400 mt-0.5" />
          <span>{localError}</span>
        </div>
      )}
    </div>
  );
}
