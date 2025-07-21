import { AnalysisRequest, AnalysisResponse } from '../types';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com' 
  : 'http://localhost:8000';

export const analyzeIngredients = async (inciList: string[]): Promise<AnalysisResponse> => {
  const payload: AnalysisRequest = {
    inci_list: inciList
  };

  try {
    const response = await fetch(`${API_BASE_URL}/analyze-inci`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    // For demo purposes, return mock data when API is not available
    console.warn('API not available, returning mock data:', error);
    return getMockResponse(inciList);
  }
};

// Mock response for development/demo purposes
const getMockResponse = (inciList: string[]): AnalysisResponse => {
  return {
    branded_ingredients: [
      {
        brand_name: "Aquaxyl",
        supplier: "Seppic",
        matched_inci: ["Xylitylglucoside", "Anhydroxylitol", "Xylitol"],
        confidence_score: 0.92,
        documentation_url: "#",
        description: "Plant-derived moisturizing complex"
      },
      {
        brand_name: "Hyaluronic Filling Spheres",
        supplier: "Infinity Labs",
        matched_inci: ["Sodium Hyaluronate Crosspolymer"],
        confidence_score: 0.87,
        documentation_url: "#",
        description: "Advanced hyaluronic acid delivery system"
      },
      {
        brand_name: "Sepilift DPHP",
        supplier: "Seppic",
        matched_inci: ["Dipalmitoyl Hydroxyproline"],
        confidence_score: 0.75,
        description: "Anti-aging peptide complex"
      }
    ],
    unmatched_inci: [
      { name: "Aqua", common_use: "Solvent", category: "Base" },
      { name: "Glycerin", common_use: "Humectant", category: "Moisturizer" },
      { name: "Phenoxyethanol", common_use: "Preservative", category: "Preservative" },
      { name: "Carbomer", common_use: "Thickener", category: "Rheology Modifier" }
    ],
    conflicts: [
      {
        inci_name: "Tocopheryl Acetate",
        possible_brands: ["Vitamin E Complex", "Tocopherol Plus"],
        context: "Could be branded or generic vitamin E"
      }
    ],
    overall_confidence: 0.84,
    processing_time: 1.2
  };
};