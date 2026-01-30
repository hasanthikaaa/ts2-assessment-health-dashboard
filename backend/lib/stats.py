import math
from typing import Optional, Dict, List

from custom_types.enums import AgeBand
from custom_types.models import Stats, EnrichedPatient, DatasetStatistics, AgeBandStats


class StatisticsComputer:
    @classmethod
    def get_age_band(cls, age: int) -> AgeBand:
        try:
            age = int(age)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid age value: {age}")

        if 0 <= age <= 17:
            return AgeBand.ZERO_TO_SEVENTEEN
        elif 18 <= age <= 39:
            return AgeBand.EIGHTEEN_TO_THIRTY_NINE
        elif 40 <= age <= 64:
            return AgeBand.FORTY_TO_SIXTY_FOUR
        elif age >= 65:
            return AgeBand.SIXTY_FIVE_PLUS
        else:
            raise ValueError(f"Invalid age value: {age}")

    @classmethod
    def compute_stats(cls, values: List[float]) -> Stats:
        if not values:
            raise ValueError("Cannot compute statistics on empty list")

        n = len(values)
        sorted_values = sorted(values)

        # Mean
        mean_value = sum(values) / n

        # Median
        mid = n // 2
        if n % 2 == 1:
            median_value = sorted_values[mid]
        else:
            median_value = (sorted_values[mid - 1] + sorted_values[mid]) / 2

        # Population standard deviation
        variance = sum((x - mean_value) ** 2 for x in values) / n
        std_dev = math.sqrt(variance)

        return Stats(mean=mean_value, median=median_value, std_dev=std_dev)

    @classmethod
    def compute_statistics(cls, patients: List[EnrichedPatient]) -> DatasetStatistics:
        total_patients = len(patients)

        age_band_values: Dict[str, Dict[str, List[float]]] = {}

        for band in AgeBand:
            age_band_values[band.value] = {
                "blood_pressure_systolic": [],
                "heart_rate": [],
                "glucose_fasting": []
            }

        for patient in patients:
            band = cls.get_age_band(patient.age).value
            age_band_values[band]["blood_pressure_systolic"].append(float(patient.blood_pressure_systolic))
            age_band_values[band]["heart_rate"].append(float(patient.heart_rate))
            age_band_values[band]["glucose_fasting"].append(float(patient.glucose_fasting))

        # Compute statistics
        age_band_stats: Dict[str, Optional[AgeBandStats]] = {}

        for band, metrics in age_band_values.items():
            band_stat = AgeBandStats(
                blood_pressure_systolic=None,
                heart_rate=None,
                glucose_fasting=None
            )

            # Compute each metric if there are values
            for key in metrics:
                values = metrics[key]
                if values:
                    try:
                        stat = cls.compute_stats(values)
                        setattr(band_stat, key, stat)
                    except ValueError:
                        setattr(band_stat, key, None)

            # if all metrics are None, set age band to None
            if (
                    band_stat.blood_pressure_systolic is None and
                    band_stat.heart_rate is None and
                    band_stat.glucose_fasting is None
               ):
                    age_band_stats[band] = None
            else:
                    age_band_stats[band] = band_stat

        return DatasetStatistics(
            total_patients=total_patients,
            age_bands=age_band_stats
        )