import { useState, Fragment } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { usePatients } from "@/contexts/PatientContext";
import RiskReasonsRow from "@/components/RiskReasonsRow";

export default function PatientTable() {
  const { patients, isLoadingPatients, error } = usePatients();
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const toggleRow = (patientId: string) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(patientId)) {
      newExpanded.delete(patientId);
    } else {
      newExpanded.add(patientId);
    }
    setExpandedRows(newExpanded);
  };

  if (isLoadingPatients) {
    return (
      <div className="patient-table">
        <div className="table-loading">Loading patients...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="patient-table">
        <div className="table-error">Error: {error}</div>
      </div>
    );
  }

  if (patients.length === 0) {
    return (
      <div className="patient-table">
        <div className="table-empty">No patients found</div>
      </div>
    );
  }

  return (
    <div className="patient-table">
      <table>
        {/* Table Header */}
        <thead>
          <tr>
            <th>Patient ID</th>
            <th>Age</th>
            <th>Gender</th>
            <th>BP (Systolic/Diastolic)</th>
            <th>BP Stage</th>
            <th>Heart Rate</th>
            <th>Risk Level</th>
            <th>Risk Score</th>
            <th>Risk Explanation</th>
          </tr>
        </thead>
        {/* Table Body */}
        <tbody>
          {patients.map((patient) => {
            const isExpanded = expandedRows.has(patient.patient_id);
            const hasReasons = patient.reasons && patient.reasons.length > 0;

            return (
              <Fragment key={patient.patient_id}>
                {/* Table Row */}
                <tr>
                  {/* Fields */}
                  <td>{patient.patient_id}</td>
                  <td>{patient.age}</td>
                  <td>{patient.gender}</td>
                  <td>
                    {patient.blood_pressure_systolic}/
                    {patient.blood_pressure_diastolic}
                  </td>
                  <td>{patient.bp_stage}</td>
                  <td>{patient.heart_rate}</td>
                  <td>
                    <span className={`risk-level risk-${patient.risk_level}`}>
                      {patient.risk_level}
                    </span>
                  </td>
                  <td>{patient.risk_score.toFixed(2)}</td>

                  {/* Risk Explanation Button */}
                  <td>
                    {hasReasons ? (
                      <button
                        type="button"
                        onClick={() => toggleRow(patient.patient_id)}
                        className="risk-explanation-btn"
                        aria-expanded={isExpanded}
                      >
                        {isExpanded ? (
                          <ChevronUp size={16} />
                        ) : (
                          <ChevronDown size={16} />
                        )}
                        <span>Why?</span>
                      </button>
                    ) : (
                      <span className="no-reasons">No reasons available</span>
                    )}
                  </td>
                </tr>
                {/* Risk Reasons Row */}
                {isExpanded && <RiskReasonsRow patient={patient} />}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
