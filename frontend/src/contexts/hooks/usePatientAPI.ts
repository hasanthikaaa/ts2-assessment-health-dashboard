import { useCallback } from "react";
import { api } from "@/lib/api";
import type {
  EnrichedPatient,
  DatasetStatistics,
  PatientFilters,
} from "@/types/alias";

export function usePatientAPI() {
  // TODO: Q5(a) - Implement getPatients function
  const getPatients = useCallback(
    async (filters: PatientFilters = {}): Promise<EnrichedPatient[]> => {
      return [];
    },
    []
  );

  // TODO: Q5(a) - Implement getStatistics function
  const getStatistics = useCallback(async (): Promise<DatasetStatistics> => {
    return {} as DatasetStatistics;
  }, []);

  return {
    getPatients,
    getStatistics,
  };
}
