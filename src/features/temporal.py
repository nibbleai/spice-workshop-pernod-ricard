import numpy as np
import pandas as pd

from src.config import config
from src.features.registry import registry
from src.features.utils import cyclical
from src.invariants import HOURS_IN_DAY
from src.schemas import TaxiColumn

from . import logger


@registry.register(name="pickup_time")
def pickup_time(data):
    """Time of pickup."""
    return data[TaxiColumn.PICKUP_TIME]


@registry.register(name="pickup_date", depends=["pickup_time"])
def pickup_date(pickup_time):
    """Date of pickup."""
    return pickup_time.dt.date


@registry.register(name="pickup_hour", depends=["pickup_time"])
def pickup_hour(pickup_time):
    """Hour of pickup."""
    return pickup_time.dt.hour


@registry.register(
    name="cyclical_pickup_hour",
    depends=["pickup_hour"]
)
def cyclical_pickup_hour(pickup_hour):
    """Hour of pickup made cyclical."""
    return cyclical(pickup_hour, cycle_length=HOURS_IN_DAY)


@registry.register(
    name="quantile_bin_hour", depends=["pickup_hour"]
)
class QuantileBinHour:
    """Quantile-based hour range of the pickup."""

    def fit(self, pickup_hour):
        hours_bins = pd.qcut(pickup_hour, q=config.features["hours_bins"])
        logger.info(f"Intervals for bins are: {hours_bins.cat.categories}")
        self.bins_ = hours_bins.cat.categories
        return self

    def transform(self, pickup_hour):
        quantile_bin_hours = pd.cut(pickup_hour, bins=self.bins_)
        hours_bins_labels = np.arange(config.features["hours_bins"]) + 1

        return quantile_bin_hours.cat.rename_categories(hours_bins_labels)
