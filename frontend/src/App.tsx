import { PatientProvider } from "@/contexts/PatientContext";
import StatisticsCards from "@/components/StatisticsCards";
import PatientFilters from "@/components/PatientFilters";
import PatientTable from "@/components/PatientTable";

export default function App() {
  return (
    <PatientProvider>
      <div className="app-container">
        {/* Statistics Cards */}
        <StatisticsCards />

        {/* Patient Filters */}
        <PatientFilters />

        {/* Patient Table */}
        <PatientTable />
      </div>
    </PatientProvider>
  );
}
