import type { EnrichedPatient } from "@/types/alias";

type RiskReasonsRowProps = {
  patient: EnrichedPatient;
};

export default function RiskReasonsRow({ patient }: RiskReasonsRowProps) {
  if (!patient.reasons || patient.reasons.length === 0) {
    return null;
  }

  return (
    <tr className="expanded-row">
      <td colSpan={9}>
        <div className="risk-reasons">
          {/* Risk Reasons Title */}
          <h4>Risk Calculation Reasons:</h4>

          {/* Risk Reasons List */}
          <ul>
            {patient.reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        </div>
      </td>
    </tr>
  );
}
