from src.features.registry import registry
from src.features.utils import cyclical
from src.invariants import HOURS_IN_DAY
from src.schemas import TaxiColumn


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
