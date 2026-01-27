import { createContext, useContext, useEffect, type ReactNode } from "react";
import { usePatientState } from "@/contexts/hooks/usePatientState";
import { usePatientAPI } from "@/contexts/hooks/usePatientAPI";
import { usePatientOperations } from "@/contexts/hooks/usePatientOperations";

type PatientContextType = {
  patients: ReturnType<typeof usePatientState>["patients"];
  statistics: ReturnType<typeof usePatientState>["statistics"];
  filters: ReturnType<typeof usePatientState>["filters"];
  isLoadingPatients: ReturnType<typeof usePatientState>["isLoadingPatients"];
  isLoadingStatistics: ReturnType<
    typeof usePatientState
  >["isLoadingStatistics"];
  error: ReturnType<typeof usePatientState>["error"];
  setFilters: ReturnType<typeof usePatientState>["setFilters"];
  fetchPatients: ReturnType<typeof usePatientOperations>["fetchPatients"];
  fetchStatistics: ReturnType<typeof usePatientOperations>["fetchStatistics"];
};

const PatientContext = createContext<PatientContextType | undefined>(undefined);

export function PatientProvider({ children }: { children: ReactNode }) {
  const state = usePatientState();
  const api = usePatientAPI();
  const operations = usePatientOperations(state, api);

  const { fetchStatistics, fetchPatients } = operations;

  // Fetch statistics on mount
  useEffect(() => {
    void fetchStatistics();
  }, [fetchStatistics]);

  // Fetch patients on mount and when filters change
  useEffect(() => {
    void fetchPatients();
  }, [fetchPatients]);

  return (
    <PatientContext.Provider
      value={{
        ...state,
        ...operations,
      }}
    >
      {children}
    </PatientContext.Provider>
  );
}

export function usePatients() {
  const context = useContext(PatientContext);
  if (context === undefined) {
    throw new Error("usePatients must be used within a PatientProvider");
  }
  return context;
}
