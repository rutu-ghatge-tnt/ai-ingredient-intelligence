import React from 'react';
import { HelpCircle } from 'lucide-react';
import { UnmatchedIngredient } from '../types';

interface UnmatchedIngredientsProps {
  ingredients: UnmatchedIngredient[];
}

const UnmatchedIngredients: React.FC<UnmatchedIngredientsProps> = ({ ingredients }) => {
  const getCategoryColor = (category?: string) => {
    switch (category) {
      case 'Base': return 'bg-blue-100 text-blue-800';
      case 'Moisturizer': return 'bg-green-100 text-green-800';
      case 'Preservative': return 'bg-orange-100 text-orange-800';
      case 'Rheology Modifier': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (ingredients.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <HelpCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>All ingredients were successfully matched to branded components</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600 mb-4">
        These ingredients appear to be generic/standalone components rather than branded complexes:
      </p>
      
      <div className="flex flex-wrap gap-3">
        {ingredients.map((ingredient, index) => (
          <div
            key={index}
            className="group relative"
          >
            <div className={`px-4 py-2 rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 transition-colors duration-200 cursor-help ${
              ingredient.common_use ? 'hover:border-gray-400' : ''
            }`}>
              <div className="flex items-center space-x-2">
                <span className="font-medium text-gray-900 text-sm">
                  {ingredient.name}
                </span>
                {ingredient.category && (
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(ingredient.category)}`}>
                    {ingredient.category}
                  </span>
                )}
              </div>
              
              {ingredient.common_use && (
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                  <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
                  Common use: {ingredient.common_use}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UnmatchedIngredients;