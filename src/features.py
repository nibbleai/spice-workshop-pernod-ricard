from spice import Registry
from src.schemas import TaxiColumn

registry = Registry("yannick")

def pickup_hour(data):
    return data[TaxiColumn.PICKUP_TIME].dt.hour
