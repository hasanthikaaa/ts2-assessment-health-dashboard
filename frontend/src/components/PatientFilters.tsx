import { useCallback } from "react";
import * as z from "zod";
import { usePatients } from "@/contexts/PatientContext";
import type {
  PatientFilters,
  RiskLevel,
  BPStage,
  AgeBand,
} from "@/types/alias";

const PatientFiltersSchema = z.object({
  risk_level: z.enum(["low", "medium", "high"]).nullable().optional(),
  bp_stage: z
    .enum(["Normal", "Elevated", "Stage 1", "Stage 2", "Hypertensive Crisis"])
    .nullable()
    .optional(),
  age_band: z.enum(["0-17", "18-39", "40-64", "65+"]).nullable().optional(),
});

export default function PatientFilters() {
  const { filters, setFilters } = usePatients();

  const handleRiskLevelChange = useCallback(
    (value: string | null) => {
      const newFilters: PatientFilters = {
        ...filters,
        risk_level: value ? (value as RiskLevel) : undefined,
      };
      if (!value) {
        delete newFilters.risk_level;
      }
      const result = PatientFiltersSchema.safeParse(newFilters);
      if (result.success) {
        setFilters(result.data);
      }
    },
    [filters, setFilters]
  );

  const handleBPStageChange = useCallback(
    (value: string | null) => {
      const newFilters: PatientFilters = {
        ...filters,
        bp_stage: value ? (value as BPStage) : undefined,
      };
      if (!value) {
        delete newFilters.bp_stage;
      }
      const result = PatientFiltersSchema.safeParse(newFilters);
      if (result.success) {
        setFilters(result.data);
      }
    },
    [filters, setFilters]
  );

  const handleAgeBandChange = useCallback(
    (value: string | null) => {
      const newFilters: PatientFilters = {
        ...filters,
        age_band: value ? (value as AgeBand) : undefined,
      };
      if (!value) {
        delete newFilters.age_band;
      }
      const result = PatientFiltersSchema.safeParse(newFilters);
      if (result.success) {
        setFilters(result.data);
      }
    },
    [filters, setFilters]
  );

  const handleClearFilters = useCallback(() => {
    setFilters({});
  }, [setFilters]);

  return (
    <div className="patient-filters">
      <div className="filters-row">
        {/* Risk Level Filter */}
        <div className="filter-group">
          <label htmlFor="risk-level">Risk Level</label>
          <select
            id="risk-level"
            value={filters.risk_level ?? ""}
            onChange={(e) => handleRiskLevelChange(e.target.value || null)}
          >
            <option value="">All</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        {/* BP Stage Filter */}
        <div className="filter-group">
          <label htmlFor="bp-stage">BP Stage</label>
          <select
            id="bp-stage"
            value={filters.bp_stage ?? ""}
            onChange={(e) => handleBPStageChange(e.target.value || null)}
          >
            <option value="">All</option>
            <option value="Normal">Normal</option>
            <option value="Elevated">Elevated</option>
            <option value="Stage 1">Stage 1</option>
            <option value="Stage 2">Stage 2</option>
            <option value="Hypertensive Crisis">Hypertensive Crisis</option>
          </select>
        </div>

        {/* Age Band Filter */}
        <div className="filter-group">
          <label htmlFor="age-band">Age Band</label>
          <select
            id="age-band"
            value={filters.age_band ?? ""}
            onChange={(e) => handleAgeBandChange(e.target.value || null)}
          >
            <option value="">All</option>
            <option value="0-17">0-17</option>
            <option value="18-39">18-39</option>
            <option value="40-64">40-64</option>
            <option value="65+">65+</option>
          </select>
        </div>

        {/* Clear Filters Button */}
        <button
          type="button"
          onClick={handleClearFilters}
          className="clear-filters-btn"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
}
