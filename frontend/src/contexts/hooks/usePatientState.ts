import { useState } from "react";
import type {
  EnrichedPatient,
  DatasetStatistics,
  PatientFilters,
} from "@/types/alias";

export function usePatientState() {
  // Data
  const [patients, setPatients] = useState<EnrichedPatient[]>([]);
  const [statistics, setStatistics] = useState<DatasetStatistics | null>(null);

  // Filters
  const [filters, setFilters] = useState<PatientFilters>({});

  // Loading
  const [isLoadingPatients, setIsLoadingPatients] = useState(false);
  const [isLoadingStatistics, setIsLoadingStatistics] = useState(false);

  // Error
  const [error, setError] = useState<string | null>(null);

  return {
    // State
    patients,
    statistics,
    filters,
    isLoadingPatients,
    isLoadingStatistics,
    error,

    // Setters
    setPatients,
    setStatistics,
    setFilters,
    setIsLoadingPatients,
    setIsLoadingStatistics,
    setError,
  };
}
