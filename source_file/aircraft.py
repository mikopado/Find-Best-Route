
class Aircraft:

    def __init__(self, model, type, manufacturer, range, fuel_capacity):
        self._model = model
        self._type = type
        self._manufacturer = manufacturer
        self._max_range = float(range)
        self._fuel_capacity = float(fuel_capacity)
        self._current_fuel = 0.0

    def get_fuel_capacity(self):
        return self._fuel_capacity

    def get_range(self):
        return self._max_range

    def get_current_fuel(self):
        return self._current_fuel

    def add_fuel(self, volume):
        """Add fuel to aircraft before flying. Checks if the quantity doesn't exceed max fuel capacity"""
        if self._current_fuel + volume >= self._fuel_capacity:
            self._current_fuel = self._fuel_capacity
        else:
            self._current_fuel += volume

    def get_fuel_consumed_per_km(self):
        return self._fuel_capacity / self._max_range

    def calculate_fuel_needed(self, km_to_do):
        """Calculate if it needs fuel to cover the input distance. Necessary for find route cheapest fuel method where it needs to
         consider if there is enough fuel in the tank to cover next trip"""
        volume = km_to_do * self.get_fuel_consumed_per_km()
        if volume <= self._current_fuel or self._current_fuel == self._fuel_capacity:
            return 0
        elif self._current_fuel <= volume < self._fuel_capacity:
            return volume - self._current_fuel
        elif volume >= self._fuel_capacity - self._current_fuel:
            return self._fuel_capacity - self._current_fuel

    def remove_fuel_consumed(self, volume):
        self._current_fuel -= volume



