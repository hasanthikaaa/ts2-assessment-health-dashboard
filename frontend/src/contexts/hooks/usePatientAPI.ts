import { useCallback } from "react";
import { api } from "@/lib/api";
import type {
  EnrichedPatient,
  DatasetStatistics,
  PatientFilters,
} from "@/types/alias";

export function usePatientAPI() {
  // Fetch patients with optional filters
  const getPatients = useCallback(
    async (filters: PatientFilters = {}): Promise<EnrichedPatient[]> => {
      try {
        const { data } = await api.get<EnrichedPatient[]>("/patients", {
          params: filters, // send filters as query parameters
        });
        return data;
      } catch (err) {
        // Re-throw to be caught in usePatientOperations
        throw err;
      }
    },
    [],
  );

  // Fetch dataset statistics
  const getStatistics = useCallback(async (): Promise<DatasetStatistics> => {
    try {
      const { data } = await api.get<DatasetStatistics>("/statistics");
      return data;
    } catch (err) {
      throw err;
    }
  }, []);

  return {
    getPatients,
    getStatistics,
  };
}
