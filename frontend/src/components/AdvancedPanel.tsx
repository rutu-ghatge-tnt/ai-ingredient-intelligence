import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Brain, TrendingUp } from 'lucide-react';

interface AdvancedPanelProps {
  overallConfidence: number;
  processingTime: number;
}

const AdvancedPanel: React.FC<AdvancedPanelProps> = ({ overallConfidence, processingTime }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const shouldShowAdvanced = overallConfidence < 0.8;

  if (!shouldShowAdvanced) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-xl p-4">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center space-x-3">
          <Brain className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900">
            Advanced Intelligence Panel
          </h3>
          <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full">
            Low Confidence Detected
          </span>
        </div>
        {isExpanded ? (
          <ChevronDown className="w-5 h-5 text-gray-600" />
        ) : (
          <ChevronRight className="w-5 h-5 text-gray-600" />
        )}
      </button>

      {isExpanded && (
        <div className="mt-6 space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg p-4 border border-purple-100">
              <h4 className="font-medium text-gray-900 mb-3 flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-purple-600" />
                <span>Analysis Metrics</span>
              </h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Overall Confidence</span>
                  <span className="font-medium text-gray-900">
                    {Math.round(overallConfidence * 100)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Processing Time</span>
                  <span className="font-medium text-gray-900">
                    {processingTime.toFixed(1)}s
                  </span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-1000"
                    style={{ width: `${overallConfidence * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-purple-100">
              <h4 className="font-medium text-gray-900 mb-3">
                Possible Hidden Branded Blends
              </h4>
              <div className="space-y-2">
                <div className="text-sm text-gray-600">
                  • Moisturizing complex detected (3-4 ingredients)
                </div>
                <div className="text-sm text-gray-600">
                  • Potential peptide blend identified
                </div>
                <div className="text-sm text-gray-600">
                  • Co-occurrence patterns suggest additional branded components
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 border border-purple-100">
            <h4 className="font-medium text-gray-900 mb-3">
              Ingredient Co-occurrence Insights
            </h4>
            <p className="text-sm text-gray-600 mb-3">
              Based on our database of formulations, these ingredient combinations frequently appear together:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-sm font-medium">Glycerin + Hyaluronic compounds</span>
                <span className="text-xs text-green-600 font-medium">High synergy</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="text-sm font-medium">Peptides + Moisturizers</span>
                <span className="text-xs text-green-600 font-medium">Common pairing</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedPanel;