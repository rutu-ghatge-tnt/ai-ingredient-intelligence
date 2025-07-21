import React from 'react';
import { Shield, Cpu } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 px-4 py-8 mt-12">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div className="flex flex-col space-y-2">
            <div className="flex items-center space-x-2">
              <Cpu className="w-4 h-4 text-indigo-600" />
              <span className="text-sm font-medium text-gray-900">
                Powered by AI
              </span>
              <span className="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs font-medium rounded">
                v1.0 Beta
              </span>
            </div>
            <p className="text-xs text-gray-500 max-w-md">
              Advanced machine learning models trained on comprehensive ingredient databases
            </p>
          </div>

          <div className="flex items-start space-x-6">
            <div className="flex items-center space-x-2">
              <Shield className="w-4 h-4 text-gray-400" />
              <div className="text-xs text-gray-500">
                <p className="font-medium">Legal Disclaimer</p>
                <p className="max-w-xs">
                  Results are AI-generated predictions for research purposes only. 
                  Verify with official documentation before formulation decisions.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-2 md:space-y-0 text-xs text-gray-500">
            <p>
              © 2025 AI Ingredient Intelligence. All rights reserved.
            </p>
            <div className="flex space-x-4">
              <button className="hover:text-gray-700 transition-colors">
                Privacy Policy
              </button>
              <button className="hover:text-gray-700 transition-colors">
                Terms of Service
              </button>
              <button className="hover:text-gray-700 transition-colors">
                API Documentation
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;