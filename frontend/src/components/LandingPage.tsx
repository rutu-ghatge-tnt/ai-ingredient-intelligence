import React from 'react';
import { 
  Microscope, 
  Brain, 
  Shield, 
  Zap, 
  Target, 
  Database,
  ArrowRight,
  CheckCircle,
  Beaker,
  TrendingUp,
  Users,
  Award
} from 'lucide-react';

interface LandingPageProps {
  onGetStarted: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning models trained on comprehensive ingredient databases for accurate identification"
    },
    {
      icon: Target,
      title: "Branded Complex Detection",
      description: "Identify proprietary ingredient blends and branded complexes from raw INCI lists with confidence scoring"
    },
    {
      icon: Database,
      title: "Comprehensive Database",
      description: "Access to extensive supplier databases including Seppic, BASF, Croda, and hundreds of specialty suppliers"
    },
    {
      icon: Shield,
      title: "Conflict Resolution",
      description: "Detect ambiguous ingredients that could belong to multiple branded complexes or be used standalone"
    }
  ];

  const useCases = [
    {
      icon: Beaker,
      title: "Formulation Analysis",
      description: "Reverse-engineer competitor products to understand their ingredient strategies"
    },
    {
      icon: TrendingUp,
      title: "Market Research",
      description: "Track trending branded ingredients and supplier preferences across the industry"
    },
    {
      icon: Users,
      title: "Supplier Intelligence",
      description: "Identify which suppliers are being used in successful formulations"
    },
    {
      icon: Award,
      title: "Quality Assurance",
      description: "Verify ingredient authenticity and detect potential formulation inconsistencies"
    }
  ];

  const steps = [
    {
      number: "01",
      title: "Input INCI List",
      description: "Paste your product's complete INCI list as it appears on the label"
    },
    {
      number: "02",
      title: "AI Analysis",
      description: "Our advanced algorithms analyze ingredient patterns and cross-reference supplier databases"
    },
    {
      number: "03",
      title: "Review Results",
      description: "Get detailed insights on branded ingredients, confidence scores, and potential conflicts"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-600/10"></div>
        <div className="relative max-w-6xl mx-auto px-4 py-16 sm:py-24">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <div className="p-4 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-lg">
                <Microscope className="w-12 h-12 text-white" />
              </div>
            </div>
            
            <h1 className="text-4xl sm:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              AI Ingredient
              <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                {" "}Intelligence
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              Unlock the secrets behind skincare formulations. Our advanced AI analyzes INCI lists 
              to identify branded ingredient complexes, supplier strategies, and formulation insights 
              that drive product innovation.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <button
                onClick={onGetStarted}
                className="group flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <span className="font-semibold text-lg">Start Analysis</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Free to use • No registration required</span>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-2xl mx-auto">
              <div className="text-center">
                <div className="text-3xl font-bold text-gray-900 mb-1">10,000+</div>
                <div className="text-sm text-gray-600">Branded Ingredients</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-gray-900 mb-1">500+</div>
                <div className="text-sm text-gray-600">Global Suppliers</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-gray-900 mb-1">95%</div>
                <div className="text-sm text-gray-600">Accuracy Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Powered by Advanced AI Technology
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our proprietary algorithms combine machine learning with comprehensive 
              ingredient databases to deliver unprecedented insights
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="group">
                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 h-full hover:shadow-lg transition-all duration-300 border border-gray-200 hover:border-indigo-200">
                    <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="py-16 bg-gradient-to-br from-indigo-50 to-purple-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Get professional-grade ingredient analysis in three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <div key={index} className="relative">
                <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-300">
                  <div className="text-4xl font-bold text-indigo-600 mb-4 opacity-20">
                    {step.number}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {step.description}
                  </p>
                </div>
                
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <ArrowRight className="w-6 h-6 text-indigo-300" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Use Cases */}
      <div className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Professional Applications
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Trusted by formulators, researchers, and industry professionals worldwide
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {useCases.map((useCase, index) => {
              const Icon = useCase.icon;
              return (
                <div key={index} className="flex items-start space-x-4 p-6 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200 hover:shadow-md transition-all duration-300">
                  <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {useCase.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {useCase.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-gradient-to-r from-indigo-600 to-purple-600">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Unlock Ingredient Intelligence?
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Join thousands of professionals who trust our AI-powered analysis 
            for their formulation research and competitive intelligence needs.
          </p>
          
          <button
            onClick={onGetStarted}
            className="group inline-flex items-center space-x-3 px-8 py-4 bg-white text-indigo-600 rounded-xl hover:bg-gray-50 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-semibold text-lg"
          >
            <span>Start Your Analysis</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
          
          <div className="mt-6 flex items-center justify-center space-x-6 text-indigo-200 text-sm">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4" />
              <span>No account required</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4" />
              <span>Instant results</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4" />
              <span>Professional grade</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;