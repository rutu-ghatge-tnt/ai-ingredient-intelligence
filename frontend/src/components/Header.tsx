import React from 'react';
import { Microscope } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 px-4 py-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center space-x-3 mb-2">
          <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg">
            <Microscope className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">
            AI Ingredient Intelligence
          </h1>
          <span className="px-2 py-1 text-xs font-medium bg-indigo-100 text-indigo-700 rounded-full">
            Beta
          </span>
        </div>
        <p className="text-gray-600 text-sm max-w-2xl">
          Identify branded ingredient complexes from INCI lists using advanced AI analysis
        </p>
      </div>
    </header>
  );
};

export default Header;