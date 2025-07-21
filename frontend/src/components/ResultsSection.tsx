import React, { useState } from 'react';
import { Package, AlertCircle, Zap } from 'lucide-react';
import { AnalysisResponse } from '../types';
import BrandedIngredients from './BrandedIngredients';
import UnmatchedIngredients from './UnmatchedIngredients';
import ConflictsSection from './ConflictsSection';

interface ResultsSectionProps {
  results: AnalysisResponse;
}

const ResultsSection: React.FC<ResultsSectionProps> = ({ results }) => {
  const [activeTab, setActiveTab] = useState<'branded' | 'unmatched' | 'conflicts'>('branded');

  const tabs = [
    {
      id: 'branded' as const,
      label: 'Branded Ingredients',
      icon: Package,
      count: results.branded_ingredients.length,
      color: 'text-indigo-600'
    },
    {
      id: 'unmatched' as const,
      label: 'Unmatched INCI',
      icon: Zap,
      count: results.unmatched_inci.length,
      color: 'text-gray-600'
    },
    {
      id: 'conflicts' as const,
      label: 'Conflicts & Ambiguities',
      icon: AlertCircle,
      count: results.conflicts.length,
      color: 'text-yellow-600'
    }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'branded':
        return <BrandedIngredients ingredients={results.branded_ingredients} />;
      case 'unmatched':
        return <UnmatchedIngredients ingredients={results.unmatched_inci} />;
      case 'conflicts':
        return <ConflictsSection conflicts={results.conflicts} />;
      default:
        return null;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Analysis Results</h2>
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-gray-600">
                Overall: {Math.round(results.overall_confidence * 100)}% confidence
              </span>
            </div>
            <div className="text-gray-500">
              {results.processing_time.toFixed(1)}s processing time
            </div>
          </div>
        </div>

        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <Icon className={`w-4 h-4 ${activeTab === tab.id ? tab.color : 'text-gray-400'}`} />
                <span>{tab.label}</span>
                {tab.count > 0 && (
                  <span className={`px-2 py-0.5 text-xs rounded-full ${
                    activeTab === tab.id 
                      ? 'bg-indigo-100 text-indigo-700' 
                      : 'bg-gray-200 text-gray-600'
                  }`}>
                    {tab.count}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <div className="p-6">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default ResultsSection;