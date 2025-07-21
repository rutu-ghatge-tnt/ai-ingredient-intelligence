import React from 'react';
import { ExternalLink, Building2, Award } from 'lucide-react';
import { BrandedIngredient } from '../types';

interface BrandedIngredientsProps {
  ingredients: BrandedIngredient[];
}

const BrandedIngredients: React.FC<BrandedIngredientsProps> = ({ ingredients }) => {
  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getConfidenceLabel = (score: number) => {
    if (score >= 0.8) return 'High';
    if (score >= 0.6) return 'Medium';
    return 'Low';
  };

  if (ingredients.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <Award className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No branded ingredients detected in this formulation</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {ingredients.map((ingredient, index) => (
        <div key={index} className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow duration-200">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h3 className="text-lg font-semibold text-gray-900">
                  {ingredient.brand_name}
                </h3>
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${getConfidenceColor(ingredient.confidence_score)}`}></div>
                  <span className="text-xs font-medium text-gray-600">
                    {getConfidenceLabel(ingredient.confidence_score)} Confidence
                  </span>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 mb-3">
                <Building2 className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-600">{ingredient.supplier}</span>
              </div>

              {ingredient.description && (
                <p className="text-sm text-gray-700 mb-3">{ingredient.description}</p>
              )}
            </div>

            <div className="text-right">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {Math.round(ingredient.confidence_score * 100)}%
              </div>
              <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className={`h-full ${getConfidenceColor(ingredient.confidence_score)} transition-all duration-500`}
                  style={{ width: `${ingredient.confidence_score * 100}%` }}
                ></div>
              </div>
            </div>
          </div>

          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Matched INCI Names:</h4>
            <div className="flex flex-wrap gap-2">
              {ingredient.matched_inci.map((inci, inciIndex) => (
                <span
                  key={inciIndex}
                  className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded-full"
                >
                  {inci}
                </span>
              ))}
            </div>
          </div>

          {ingredient.documentation_url && (
            <div className="flex justify-end">
              <a
                href={ingredient.documentation_url}
                className="flex items-center space-x-1 text-sm text-indigo-600 hover:text-indigo-700"
                target="_blank"
                rel="noopener noreferrer"
              >
                <span>View Documentation</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default BrandedIngredients;