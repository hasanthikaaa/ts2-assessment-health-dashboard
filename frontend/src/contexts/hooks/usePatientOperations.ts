import { useCallback } from "react";
import type { usePatientState } from "@/contexts/hooks/usePatientState";
import type { usePatientAPI } from "@/contexts/hooks/usePatientAPI";
import type { PatientFilters } from "@/types/alias";

export function usePatientOperations(
  state: ReturnType<typeof usePatientState>,
  api: ReturnType<typeof usePatientAPI>,
) {
  const {
    setPatients,
    setStatistics,
    setIsLoadingPatients,
    setIsLoadingStatistics,
    setError,
    filters,
  } = state;

  const { getPatients, getStatistics } = api;

  // Fetch patients with current filters
  const fetchPatients = useCallback(async () => {
    setIsLoadingPatients(true);
    setError(null);
    try {
      const data = await getPatients(filters as PatientFilters);
      setPatients(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to fetch patients");
      }
    } finally {
      setIsLoadingPatients(false);
    }
  }, [filters, getPatients, setPatients, setIsLoadingPatients, setError]);

  // Fetch dataset statistics
  const fetchStatistics = useCallback(async () => {
    setIsLoadingStatistics(true);
    setError(null);
    try {
      const statsData = await getStatistics();
      setStatistics(statsData);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to fetch statistics");
      }
    } finally {
      setIsLoadingStatistics(false);
    }
  }, [getStatistics, setStatistics, setIsLoadingStatistics, setError]);

  return {
    fetchPatients,
    fetchStatistics,
  };
}
