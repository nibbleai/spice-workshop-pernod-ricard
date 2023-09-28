from spice import Registry

registry = Registry('nyc-taxi')

@registry.register(depends="pick_up_time")
def pick_up_hour(pick_up_time):
    return pick_up_time.dt.hour

@registry.register(depends="pick_up_time")
def pick_up_day(pick_up_time):
    return pick_up_time.dt.day

@registry.register()
def pick_up_time(data):
    return data.pickup_datetime
