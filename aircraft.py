
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

    def add_fuel(self, km_to_do):
        """Add fuel to aircraft before flying. Checks if the quantity doesn't exceed max fuel capacity"""
        quantity_to_add = km_to_do * self.get_fuel_consumed_per_km()
        if self._current_fuel + quantity_to_add >= self._fuel_capacity:
            self._current_fuel = self._fuel_capacity
        else:
            self._current_fuel += quantity_to_add

    def get_fuel_consumed_per_km(self):
        return self._fuel_capacity / self._max_range

    # def calculate_fuel_needed(self, km_to_do):
    #     quantity = km_to_do * self.get_fuel_consumed_per_km()
    #     if self._current_fuel <= quantity < self._fuel_capacity:
    #         return quantity - self._current_fuel
    #     elif quantity >= self._fuel_capacity - self._current_fuel:
    #         return self._fuel_capacity - self._current_fuel

    def remove_fuel_consumed(self, km_flown):
        fuel_used = km_flown * self.get_fuel_consumed_per_km()
        self._current_fuel -= fuel_used

    def get_current_range(self):
        return self._current_fuel * self._max_range / self._fuel_capacity


