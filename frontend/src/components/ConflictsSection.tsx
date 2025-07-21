import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { ConflictIngredient } from '../types';

interface ConflictsSectionProps {
  conflicts: ConflictIngredient[];
}

const ConflictsSection: React.FC<ConflictsSectionProps> = ({ conflicts }) => {
  if (conflicts.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <AlertTriangle className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No conflicting ingredient mappings detected</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600 mb-4">
        These ingredients could belong to multiple branded complexes or be used standalone:
      </p>
      
      {conflicts.map((conflict, index) => (
        <div key={index} className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 mb-2">
                {conflict.inci_name}
              </h4>
              
              <div className="mb-3">
                <span className="text-sm text-gray-600">Possible brands: </span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {conflict.possible_brands.map((brand, brandIndex) => (
                    <span
                      key={brandIndex}
                      className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded"
                    >
                      {brand}
                    </span>
                  ))}
                </div>
              </div>

              {conflict.context && (
                <p className="text-sm text-gray-600 italic">
                  {conflict.context}
                </p>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ConflictsSection;