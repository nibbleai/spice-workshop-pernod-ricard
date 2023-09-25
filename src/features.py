from spice import Registry
from src.schemas import TaxiColumn

registry = Registry("yannick")

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
