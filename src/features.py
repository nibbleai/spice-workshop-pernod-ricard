from spice import Registry
from src.schemas import TaxiColumn
import numpy as np
import pandas as pd

registry = Registry("yannick")


def cyclical(data, *, cycle_length):
    ratio = data * (2 * np.pi / cycle_length)
    return {
        'sin': np.sin(ratio),
        'cos': np.cos(ratio)
    }


@registry.register(
        depends=["pickup_hour"]
)
def cyclical_pick_hour(pickup_hour):
    return cyclical(pickup_hour, cycle_length=24)


# par défaut le nom de la feature sera le nom de la fonction
@registry.register(
    depends=["pickup_time"],
) # enregistre la fonction dans le registry
def pickup_hour(pickup_time):
    return pickup_time.dt.hour


@registry.register(
    depends=["pickup_time"],
)
def pickup_year(pickup_time):
    return pickup_time.dt.year


@registry.register(name="pickup_time")
def pickup_time(data):
    return data[TaxiColumn.PICKUP_TIME]


@registry.register(depends=["pickup_hour"])
def bin_cut_hour(pickup_hour):
    bins = np.arange(0, 25, 6)

    return pd.cut(
        pickup_hour,
        bins=bins,
        labels=np.arange(1, 5),
        right=False
    )


@registry.register(
    name="quantile_hour",
    depends=["pickup_hour"]
)
class QuantileHour:

    def fit(self, pickup_hour):
        self.hours_bins = pd.qcut(pickup_hour, q=4).cat.categories

    def transform(self, pickup_hour):
        return pd.cut(pickup_hour, bins=self.hours_bins)
