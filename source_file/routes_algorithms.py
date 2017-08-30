import sys

from source_file.custom_exceptions import *

class Routes:
    def __init__(self,aircrafts, airports, currency_rates, currencies):
        self._aircrafts = aircrafts
        self._airports = airports
        self._currency_rates = currency_rates
        self._currencies = currencies

    def count_visited_airports(self, aDict, anAirportCode):
        """Counts how many times an airport code appears as a departure airport in route dictionary"""
        count = 0
        for sequence in aDict.values():
            if anAirportCode == sequence[0]:
                count += 1
        return count

    def modify_list(self, airports_list, aDict):
        """Modify an input list if any element of this list is also inside a values of a given dictionary"""
        newList = airports_list[:]
        for i in airports_list:
            for j in aDict.values():
                if i in j and i in newList:
                    newList.remove(i)
        return newList

    def calculate_sum_km_or_fuel_in_best_route(self, route, index):
        """Calculates the sum of parameters in route dictionary (e.g. total amount of km, euro, liter)"""
        sum = 0
        for j in route.values():
            sum += j[index]
        return round(sum, 2)

    def find_shortest_route(self, aircraft_model, departure, airports):
        """Function that determine the best route from a alist of airports based on the minumum distance beetween airports.
        Basically For each departure airport it will find the airport at minimum distance and selects this airport as arrival airport.
        """
        trip = 1
        takeoff_code = departure
        km_to_do = 0
        best_route = {}
        aircraft = self._aircrafts.get_object_from_key(aircraft_model)
        number_trip = 6
        while trip < number_trip:
            min_distance = sys.maxsize
            destination = departure
            takeoff_rate = self._currency_rates.get_rate_from_country(takeoff_code, self._airports, self._currencies)

            for airp in airports:
                distance_airports = self._airports.get_distance_between_airports(takeoff_code, airp)

                if distance_airports <= aircraft.get_range():
                    """For each airport in the list if the distance to departure airport is less than aircraft range and this
                    distance is the smallest among other airports, this airport will be the next destination.
                     Distance must be greater than zero, means it's not considering the departure airport as arrival airport."""
                    if min_distance > distance_airports > 0:
                        destination = airp
                        min_distance = distance_airports

            km_to_do = self._airports.get_distance_between_airports(takeoff_code, destination)
            best_route = self.carry_out_trip_airport_to_airport(aircraft, km_to_do, takeoff_rate, takeoff_code,
                                                                destination, best_route, trip)

            takeoff_code = destination

            trip += 1
            airports = self.modify_list(airports, best_route)
            if destination == departure:
                break

        if len(airports) > 0 or km_to_do > aircraft.get_range():
            best_route = {}

        return best_route

    def get_airport_at_min_distance_within_range(self, takeoff_code, destination, aircraft, airports):
        """Gets the airport at minimum distance from takeoof code airport considering the aircraft range"""
        min_distance = sys.maxsize
        for target_code in airports:
            target_airp_distance = self._airports.get_distance_between_airports(takeoff_code, target_code)
            if target_code != takeoff_code and target_airp_distance <= aircraft.get_range() and target_airp_distance < min_distance:
                destination = target_code
                min_distance = target_airp_distance
        return destination

    def find_route_with_possible_stopover(self, aircraft_model, departure, airports):
        """
            A method that returns a dictionary representing the best route among five airports for a selected aircraft.
            Input: aircraft model --- string
                    home_code  ---- string representing the starting and ending point of the route
                    airport_list ---- list of four airports where the aircraft should visit for completing the route
            Output: best_route --- dictionary with key equal to number of trip and values a tuple containing
            (departure airport, arrival airport, distance between airports, cost of fuel in euro)

            """
        """ Explanation of the algorithm:
        For each departure airport it finds the airport at maximum distance to it. Then if this distance is higher than
        the aircraft range, it will check if there is any airport between them at distance less than aircraft range and at
        convenient rate. If it finds this airport the algorithm already has identified two trips. If it doesn't find any airport
        in between to split the largest distance, it will find an airport at minimum distance.
        If the distance between departure airport to its furthest airport is less than aircraft range, it will check first of all
        if the currency rate at departure airport is cheaper than arrival airport, in this case arrival airport it will be
        equal to the furthest airport. Otherwise it will find the airport at minimum distance
        """
        aircraft = self._aircrafts.get_object_from_key(aircraft_model)
        takeoff_airp = departure
        distance_airports = 0
        best_route = {}
        list_stopover = airports[:]  # supporting list
        trip = 1
        cheapest_rate = self._currency_rates.get_cheapest_rate_from_airport_codes([*airports, departure], self._airports,
                                                                                  self._currencies)
        airport_already_visited = False
        number_trips = 7

        while trip < number_trips:
            destination = ''
            takeoff_rate = self._currency_rates.get_rate_from_country(takeoff_airp, self._airports, self._currencies)
            fuel_rate = takeoff_rate

            airport_max = self.set_airport_at_max_distance(airports, departure, takeoff_airp)

            distance_airports = self._airports.get_distance_between_airports(takeoff_airp, airport_max)

            list_stopover = self.delete_airport_from_stopover(best_route, takeoff_airp, airport_already_visited, list_stopover, airports)

            best_price = takeoff_rate * distance_airports
            destination, distance_airports = self.find_stopover_between_airports(list_stopover, takeoff_airp, airport_max, aircraft,
                                                                        takeoff_rate, destination, distance_airports, best_price, best_route)

            if destination != '':
                """If destination code is equal to empty string, it means program didn't find any airport
                    in the previous iteration. In this case it will check for airport at closest distance to departure
                    airport otherwise it will store two trips in best_route dictionary"""
                # Set all parameters for first trip from takeoff airport to the airport in between with airport max
                best_route = self.carry_out_trip_airport_to_airport(aircraft, distance_airports, fuel_rate,
                                                                             takeoff_airp, destination,
                                                                             best_route, trip)
                airports = self.modify_list(airports, best_route)
                trip += 1
                # Begins to set up next trip between the middle destination to airport max
                takeoff_airp = destination
                if self.count_visited_airports(best_route, takeoff_airp) >= 1:
                    airport_already_visited = True
                destination = airport_max
                fuel_rate = self._currency_rates.get_rate_from_country(takeoff_airp, self._airports, self._currencies)
            else:
                """If the distance between farthest airport and the departure airport is less than aircraft range, then
                   it checks first if the departure airport has better rate, if so next destination will be farthest airport,
                   otherwise it will check for a closest airport"""
                if distance_airports <= aircraft.get_range():
                    if airport_max == departure:
                        destination = departure
                    elif takeoff_rate <= cheapest_rate:
                        destination = airport_max
                    else:
                        destination = self.get_airport_at_min_distance_within_range(takeoff_airp, destination, aircraft,
                                                                               list_stopover)
                else:
                    break

            # Set parameters for nth trip and store in the route
            distance_airports = self._airports.get_distance_between_airports(takeoff_airp, destination)
            best_route = self.carry_out_trip_airport_to_airport(aircraft, distance_airports, fuel_rate, takeoff_airp,
                                                                         destination, best_route, trip)
            airports = self.modify_list(airports, best_route)
            takeoff_airp = destination

            if destination == departure:
                break
            trip += 1
        if len(airports) > 0 or distance_airports > aircraft.get_range():
            """At the end of the while loop programs check if there is still some airports which hasn't been visited or
            if the last trip to the ending airport is less than aircraft range"""
            best_route = {}

        return best_route


    def find_stopover_between_airports(self, list_stopover, takeoff_airport, airport_max, aircraft,
                                       takeoff_rate, destination, distance, best_price, best_route):

        for airp in list_stopover:
            """For each airport still in the stop over list, it checks if there is any airport between
               the departure and its farthest airport. If this airport is at the distance to each of them less
               than aircraft range and it's the most convenient then the program chooses this airport and get two trips.
                First trip - departure to selected airport and second trip - selected airport to farthest airport
            """
            if airp != takeoff_airport and airp != airport_max and self.count_visited_airports(best_route, takeoff_airport) < 1:

                distance_takeoff_airp = self._airports.get_distance_between_airports(takeoff_airport, airp)
                distance_airp_airpmax = self._airports.get_distance_between_airports(airp, airport_max)
                airp_rate = self._currency_rates.get_rate_from_country(airp, self._airports, self._currencies)

                if distance_airp_airpmax <= aircraft.get_range() and distance_takeoff_airp <= aircraft.get_range():
                    if takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate < best_price:
                        destination = airp
                        best_price = takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate
                        distance = distance_takeoff_airp

        return destination, distance


    def carry_out_trip_airport_to_airport(self, aircraft, distance, fuel_rate, departure, destination, best_route, trip_num):
        fuel_needed = aircraft.calculate_fuel_needed(distance)
        cost_fuel = fuel_needed * fuel_rate
        aircraft.add_fuel(fuel_needed)
        best_route[trip_num] = (departure, destination, distance, cost_fuel, fuel_needed)
        aircraft.remove_fuel_consumed(distance * aircraft.get_fuel_consumed_per_km())
        return best_route

    def set_airport_at_max_distance(self, airports, home_code, takeoff_code):
        if len(airports) == 0:
            airport_max = home_code
        else:
            airport_max = self._airports.get_airport_at_max_distance(takeoff_code, airports)
        return airport_max

    def delete_airport_from_stopover(self, best_route, takeoff_code, is_visited, stopovers, airports):
        if self.count_visited_airports(best_route, takeoff_code) >= 1:
            # Check if some airports have been visited twice. If so modifies the list of possible stopover
            is_visited = True
        if is_visited:
            stopovers = airports
        return stopovers

    def calculate_total_longest_distance(self, airports):
        """Calculates the sum of all the airports at the maximum distance for each airport in the list"""
        #airport_dict = AirportAtlas('../csv_files/airport.csv')
        total_distance = 0
        for code in airports:
            farthest_airp = self._airports.get_airport_at_max_distance(code, airports)
            total_distance += self._airports.get_distance_between_airports(code, farthest_airp)
        return total_distance

    def find_route_saving_fuel(self, aircraft_model, departure, airports):
        """This method it will find the cheapest route considering the fuel capacity of the aircraft. The primary goal is to find always the cheapest
        airport and heading towards it. After getting the cheapest airport the aircraft will be filled it up to save money when
        the route will hit a pricey airport. The algorithm considers to not fill it up to the max capacity as this will be more
        expensive in case where the route is very short. Therefore it has been calculate a longest distance that allow to fill itup
        to total maximum distance between the airports still in the list (i.e they still need to be visited)
        """
        aircraft = self._aircrafts.get_object_from_key(aircraft_model)
        longest_distance = self.calculate_total_longest_distance([*airports, departure])
        takeoff_airport = departure
        trip = 1
        distance_airports = 0
        best_route = {}
        number_trips = 6
        while trip < number_trips:
            destination = departure
            takeoff_rate = self._currency_rates.get_rate_from_country(takeoff_airport, self._airports, self._currencies)
            cheapest_airp = self.get_cheapest_airport_at_min_distance(takeoff_airport, airports)

            if len(airports) > 0:
                dist_takeoff_cheapest = self._airports.get_distance_between_airports(takeoff_airport, cheapest_airp)
                airp_at_max_dist = self._airports.get_airport_at_max_distance(takeoff_airport, airports)
                """If the departure airport is not the cheapest and the cheapest airport is not at its maximum distance, then
                the destination airport it will be the cheapest airport. Otherwise if the departure airport is the cheapest then
                the aircraft will fly to the airport at maximum distance from departure airport. Otherwise it will find any airport
                that is not at maximum distance and still in the aircraft range"""
                if takeoff_airport != cheapest_airp and dist_takeoff_cheapest <= aircraft.get_range() and cheapest_airp != airp_at_max_dist:
                    destination = cheapest_airp
                elif takeoff_airport == cheapest_airp and dist_takeoff_cheapest <= aircraft.get_range():
                    dist_takeoff_airp_max = self._airports.get_distance_between_airports(takeoff_airport, airp_at_max_dist)
                    destination = self.find_airport_within_aircraft_range(aircraft, airports, dist_takeoff_airp_max,
                                                                          takeoff_airport, airp_at_max_dist, destination)

                else:
                    cheapest_route = sys.maxsize
                    destination, distance_airports = self.find_stopover_between_airports(airports, takeoff_airport, airp_at_max_dist,
                                                                                aircraft, takeoff_rate,
                                                                                destination, distance_airports, cheapest_route, best_route)

                    # Set parameters for first trip from departure to the airport between departure and cheapest airport
                    best_route = self.carry_out_trip_airport_to_airport(aircraft, distance_airports, takeoff_rate, takeoff_airport, destination, best_route, trip)

                    airports = self.modify_list(airports, best_route)

                    if destination == departure:
                        break
                    # Modify longest distance considering the new list, therefore without the departure airport
                    longest_distance = self.calculate_total_longest_distance([*airports, departure])
                    takeoff_airport = destination
                    destination = cheapest_airp
                    trip += 1

            distance_airports = self._airports.get_distance_between_airports(takeoff_airport, destination)
            """If departure is the cheapest aiport then fill the aircraft up to the longest distance, otherwise only the necessary fuel to
            get the next airport"""
            if takeoff_airport == cheapest_airp:
                fuel_needed = aircraft.calculate_fuel_needed(longest_distance)
                aircraft.add_fuel(fuel_needed)
            else:
                fuel_needed = aircraft.calculate_fuel_needed(distance_airports)
                aircraft.add_fuel(fuel_needed)

            # Set parameters for nth trip and store data in best_route dictionary.
            cost_fuel = fuel_needed * takeoff_rate
            best_route[trip] = (takeoff_airport, destination, distance_airports, cost_fuel, fuel_needed)
            aircraft.remove_fuel_consumed(distance_airports * aircraft.get_fuel_consumed_per_km())
            airports = self.modify_list(airports, best_route)
            longest_distance = self.calculate_total_longest_distance([*airports, departure])
            takeoff_airport = destination
            trip += 1
            if destination == departure:
                break
        if distance_airports > aircraft.get_range() or len(airports) > 0:
            # If after searching the route there is still any airport that has not been visited, or the distance last airport
            #  go back home is greater than maximum aircraft range then delete route found as it's not valuable
            best_route = {}
        return best_route

    def find_airport_within_aircraft_range(self, aircraft, airports, dist_takeoff_airp_max, takeoff_airport,
                                           airp_at_max_dist, destination):
        while dist_takeoff_airp_max > aircraft.get_range():
            airports_in_range = [code for code in airports if
                         self._airports.get_distance_between_airports(takeoff_airport,
                                                                      code) < dist_takeoff_airp_max]
            if len(airports_in_range) > 0:
                airp_at_max_dist = self._airports.get_airport_at_max_distance(takeoff_airport, airports_in_range)
                dist_takeoff_airp_max = self._airports.get_distance_between_airports(takeoff_airport,
                                                                                     airp_at_max_dist)
            else:
                break
        else:
            destination = airp_at_max_dist

        return destination

    def get_cheapest_airport_at_min_distance(self, home_airport, airports):
        airports = [*airports, home_airport]
        cheapest_rate = self._currency_rates.get_cheapest_rate_from_airport_codes(airports, self._airports,
                                                                                  self._currencies)
        list_cheapest = []
        for airp in airports:
            if self._currency_rates.get_rate_from_country(airp, self._airports, self._currencies) == cheapest_rate:
                list_cheapest.append(airp)
        if len(list_cheapest) == 1:
            return list_cheapest[0]
        else:
            return self._airports.get_airport_at_min_distance(home_airport, list_cheapest)

    def find_cheapest_route(self, aircraft_model, home_airport, airports):
        """Gathers the three find route methods and it will find the cheapest route for the selected list of airports.
        This is the main method which it will run on GUI"""
        list_routes = []
        #currency_rates = CurrencyRatesDictionaryParent('../csv_files/currencyrates.csv')
        #currencies = CountryCurrenciesDictionaryParent('../csv_files/countrycurrency.csv')
        list_routes.append(self.find_route_with_possible_stopover(aircraft_model, home_airport, airports))

        list_routes.append(self.find_shortest_route(aircraft_model, home_airport, airports))
        list_routes.append(self.find_route_saving_fuel(aircraft_model, home_airport, airports))
        best_price = sys.maxsize
        best_route = {}
        for i in list_routes:
            if 0 != self.calculate_sum_km_or_fuel_in_best_route(i, 3) < best_price:
                best_price = self.calculate_sum_km_or_fuel_in_best_route(i, 3)
                best_route = i
        if best_route == {}:
            raise RouteNotFoundError('Sorry. No route found for this aircraft to the selected destinations.')

        return self.get_info_best_route(best_route)

    def get_info_best_route(self, route_dict):
        """Method to display information of the various airport in the route"""
        output_route = {}
        for trip, route in route_dict.items():
            dep_airp = self._airports.get_object_from_key(route[0]).__str__()
            arr_airp = self._airports.get_object_from_key(route[1]).__str__()
            cost = round(route[3], 2)
            fuel = round(route[4], 2)
            output_route[trip] = (dep_airp, arr_airp, route[2], cost, fuel)
        return output_route
