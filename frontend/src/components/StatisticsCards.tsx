import { usePatients } from "@/contexts/PatientContext";

const AGE_BANDS = ["0-17", "18-39", "40-64", "65+"] as const;

export default function StatisticsCards() {
  const { statistics, isLoadingStatistics } = usePatients();

  if (isLoadingStatistics) {
    return (
      <div className="statistics-cards">
        <div className="statistics-loading">Loading statistics...</div>
      </div>
    );
  }

  if (!statistics) {
    return (
      <div className="statistics-cards">
        <div className="statistics-error">No statistics available</div>
      </div>
    );
  }

  return (
    <div className="statistics-cards">
      {/* Statistics Header */}
      <div className="statistics-header">
        <h2>Dataset Statistics</h2>
        <div className="total-patients">
          Total Patients: <strong>{statistics.total_patients}</strong>
        </div>
      </div>

      {/* Age Bands Grid */}
      <div className="age-bands-grid">
        {AGE_BANDS.map((ageBand) => {
          const bandStats = statistics.age_bands[ageBand];
          if (!bandStats) {
            return null;
          }
          return (
            <div key={ageBand} className="age-band-card">
              {/* Age Band Title */}
              <h3 className="age-band-title">Age {ageBand}</h3>

              {/* Age Band Stats */}
              <div className="age-band-stats">
                {/* Systolic BP Stat */}
                {bandStats.blood_pressure_systolic && (
                  <div className="stat-item">
                    <span className="stat-label">Systolic BP:</span>
                    <span className="stat-value">
                      Mean: {bandStats.blood_pressure_systolic.mean.toFixed(1)},
                      Median:{" "}
                      {bandStats.blood_pressure_systolic.median.toFixed(1)}
                    </span>
                  </div>
                )}

                {/* Heart Rate Stat */}
                {bandStats.heart_rate && (
                  <div className="stat-item">
                    <span className="stat-label">Heart Rate:</span>
                    <span className="stat-value">
                      Mean: {bandStats.heart_rate.mean.toFixed(1)}, Median:{" "}
                      {bandStats.heart_rate.median.toFixed(1)}
                    </span>
                  </div>
                )}

                {/* Fasting Glucose Stat */}
                {bandStats.glucose_fasting && (
                  <div className="stat-item">
                    <span className="stat-label">Fasting Glucose:</span>
                    <span className="stat-value">
                      Mean: {bandStats.glucose_fasting.mean.toFixed(1)}, Median:{" "}
                      {bandStats.glucose_fasting.median.toFixed(1)}
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
