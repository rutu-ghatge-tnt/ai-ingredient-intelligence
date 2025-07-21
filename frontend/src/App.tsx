import React, { useState } from 'react';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import InputPanel from './components/InputPanel';
import ResultsSection from './components/ResultsSection';
import AdvancedPanel from './components/AdvancedPanel';
import Footer from './components/Footer';
import { analyzeIngredients } from './services/api';
import { AnalysisState } from './types';

function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    isLoading: false,
    results: null,
    error: null
  });

  const handleGetStarted = () => {
    setShowLanding(false);
  };

  const handleAnalyze = async (inciList: string[]) => {
    setAnalysisState({ isLoading: true, results: null, error: null });

    try {
      const results = await analyzeIngredients(inciList);
      setAnalysisState({ isLoading: false, results, error: null });
    } catch (error) {
      setAnalysisState({
        isLoading: false,
        results: null,
        error: error instanceof Error ? error.message : 'An unexpected error occurred'
      });
    }
  };

  if (showLanding) {
    return (
      <div className="min-h-screen">
        <LandingPage onGetStarted={handleGetStarted} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        <InputPanel 
          onAnalyze={handleAnalyze} 
          isLoading={analysisState.isLoading} 
        />

        {analysisState.error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
              <span className="text-red-800 font-medium">Analysis Error</span>
            </div>
            <p className="text-red-700 text-sm mt-2">{analysisState.error}</p>
          </div>
        )}

        {analysisState.results && (
          <>
            <ResultsSection results={analysisState.results} />
            <AdvancedPanel 
              overallConfidence={analysisState.results.overall_confidence}
              processingTime={analysisState.results.processing_time}
            />
          </>
        )}

        {!analysisState.results && !analysisState.isLoading && !analysisState.error && (
          <div className="text-center py-16">
            <div className="max-w-md mx-auto">
              <div className="w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full opacity-20"></div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Ready to Analyze
              </h3>
              <p className="text-gray-600 text-sm">
                Paste your INCI list above to discover branded ingredient complexes 
                and get detailed analysis of your formulation
              </p>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;