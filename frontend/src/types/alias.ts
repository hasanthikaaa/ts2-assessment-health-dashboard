import type { components } from "@/types/api";

// Enums
export type RiskLevel = components["schemas"]["RiskLevel"];
export type BPStage = components["schemas"]["BPStage"];
export type AgeBand = components["schemas"]["AgeBand"];
export type Gender = components["schemas"]["Gender"];
export type Stats = components["schemas"]["Stats"];

// Schemas
export type EnrichedPatient = components["schemas"]["EnrichedPatient"];
export type DatasetStatistics = components["schemas"]["DatasetStatistics"];
export type AgeBandStats = components["schemas"]["AgeBandStats"];

// Filters
export type PatientFilters = {
  risk_level?: RiskLevel | null;
  bp_stage?: BPStage | null;
  age_band?: AgeBand | null;
};

// Error Response
export type ErrorResponse = {
  detail: string;
};
