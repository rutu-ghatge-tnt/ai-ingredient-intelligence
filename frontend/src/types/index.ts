export interface AnalysisRequest {
  inci_list: string[];
}

export interface BrandedIngredient {
  brand_name: string;
  supplier: string;
  matched_inci: string[];
  confidence_score: number;
  documentation_url?: string;
  description?: string;
}

export interface UnmatchedIngredient {
  name: string;
  common_use?: string;
  category?: string;
}

export interface ConflictIngredient {
  inci_name: string;
  possible_brands: string[];
  context?: string;
}

export interface AnalysisResponse {
  branded_ingredients: BrandedIngredient[];
  unmatched_inci: UnmatchedIngredient[];
  conflicts: ConflictIngredient[];
  overall_confidence: number;
  processing_time: number;
}

export interface AnalysisState {
  isLoading: boolean;
  results: AnalysisResponse | null;
  error: string | null;
}