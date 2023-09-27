import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from src.config import config
from src.features.registry import registry
from src.schemas import TaxiColumn

from . import logger


@registry.register(name="pickup_lon")
def pickup_longitude(data):
    """Longitude of pickup position."""
    return data[TaxiColumn.PICKUP_LON]


@registry.register(name="pickup_lat")
def pickup_latitude(data):
    """Latitude of pickup position."""
    return data[TaxiColumn.PICKUP_LAT]


@registry.register(name="dropoff_lon")
def dropoff_longitude(data):
    """Longitude of dropoff position."""
    return data[TaxiColumn.DROPOFF_LON]


@registry.register(name="dropoff_lat")
def dropoff_latitude(data):
    """Latitude of dropoff position."""
    return data[TaxiColumn.DROPOFF_LAT]


@registry.register(
    name="euclidean_distance",
    depends=["pickup_lon", "pickup_lat", "dropoff_lon", "dropoff_lat"]
)
def euclidean_distance(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    """Euclidean distance between pickup & dropoff positions."""
    return np.sqrt(
        abs(pickup_lon - dropoff_lon) ** 2 + abs(pickup_lat - dropoff_lat) ** 2
    )

@registry.register(
    name="manhattan_distance",
    depends=["pickup_lon", "pickup_lat", "dropoff_lon", "dropoff_lat"]
)
def manhattan_distance(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    """Manhattan distance between pickup & dropoff positions."""
    return abs(pickup_lon - dropoff_lon) + abs(pickup_lat - dropoff_lat)


@registry.register(name="pickup_cluster", depends=["pickup_lon", "pickup_lat"])
class PickupCluster:
    """Quantile-based hour range of the pickup."""

    def fit(self, pickup_lon, pickup_lat):
        n = config.features["pickup_n_clusters"]
        logger.info(f"Fitting Kmeans with {n} clusters")
        self.kmeans_ = KMeans(n_clusters=n)
        self.kmeans_.fit(pd.concat([pickup_lon, pickup_lat], axis=1))
        return self

    def transform(self, pickup_lon, pickup_lat):
        coords = pd.concat([pickup_lon, pickup_lat], axis=1)
        return pd.Categorical(self.kmeans_.predict(coords))
