import React, { useState } from 'react';
import { Search, Upload, Loader2 } from 'lucide-react';

interface InputPanelProps {
  onAnalyze: (inciList: string[]) => void;
  isLoading: boolean;
}




const InputPanel: React.FC<InputPanelProps> = ({ onAnalyze, isLoading }) => {
  const [inputText, setInputText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    // Parse INCI list - split by commas and clean up
    const inciList = inputText
      .split(',')
      .map(item => item.trim())
      .filter(item => item.length > 0);

    onAnalyze(inciList);
  };

  const handleExampleClick = () => {
    const exampleINCI = "Aqua, Glycerin, Xylitylglucoside, Anhydroxylitol, Xylitol, Sodium Hyaluronate Crosspolymer, Dipalmitoyl Hydroxyproline, Tocopheryl Acetate, Phenoxyethanol, Carbomer, Triethanolamine";
    setInputText(exampleINCI);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="mb-4">
        <label htmlFor="inci-input" className="block text-sm font-semibold text-gray-900 mb-2">
          Paste your product's INCI list
        </label>
        <p className="text-xs text-gray-500 mb-3">
          Enter ingredients separated by commas, as they appear on your product label
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            id="inci-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="e.g. Aqua, Glycerin, Sorbitan Laurate, Lauroyl Proline, Sodium Hyaluronate..."
            className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none text-sm"
            disabled={isLoading}
          />
          <div className="absolute bottom-3 right-3">
            <button
              type="button"
              onClick={handleExampleClick}
              className="text-xs text-indigo-600 hover:text-indigo-700 underline"
              disabled={isLoading}
            >
              Try example
            </button>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              type="submit"
              disabled={!inputText.trim() || isLoading}
              className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Search className="w-4 h-4" />
              )}
              <span className="font-medium">
                {isLoading ? 'Analyzing...' : 'Analyze Ingredients'}
              </span>
            </button>

            <div className="relative">
              <button
                type="button"
                disabled
                className="flex items-center space-x-2 px-4 py-3 bg-gray-100 text-gray-400 rounded-lg cursor-not-allowed"
                title="Coming soon: Extract ingredients from documents"
              >
                <Upload className="w-4 h-4" />
                <span className="text-sm">Upload TDS</span>
              </button>
            </div>
          </div>

          {inputText && (
            <div className="text-xs text-gray-500">
              {inputText.split(',').filter(item => item.trim()).length} ingredients detected
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default InputPanel;