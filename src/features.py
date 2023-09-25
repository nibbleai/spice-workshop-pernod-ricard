from spice import Registry
from src.schemas import TaxiColumn
import numpy as np

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
