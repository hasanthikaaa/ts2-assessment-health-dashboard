import math
from typing import Optional, Dict, List

from custom_types.enums import AgeBand
from custom_types.models import Stats, EnrichedPatient, DatasetStatistics, AgeBandStats


class StatisticsComputer:
    # TODO: Q2(a) - Implement get_age_band method
    def get_age_band(cls, age: int) -> AgeBand:
        pass

    # TODO: Q2(b) - Implement compute_stats method
    def compute_stats(cls, values: List[float]) -> Stats:
        pass

    # TODO: Q2(c) - Implement compute_statistics method
    def compute_statistics(cls, patients: List[EnrichedPatient]) -> DatasetStatistics:
        pass
