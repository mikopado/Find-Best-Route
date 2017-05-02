import sys
from airport_atlas import AirportAtlas
from currency_rates import CurrencyRatesDictionaryParent
from country_currencies import CountryCurrenciesDictionaryParent
from custom_exceptions import *
"""This file gathers all the algorithms used to find the best and cheapest route. Along with them there are some supporting
methods that help to finalize the algorithms themselves"""

def count_visited_airports(aDict, anAirportCode):
    """Counts how many times an airport code appears as a departure airport in route dictionary"""
    count = 0
    for sequence in aDict.values():
        if anAirportCode == sequence[0]:
            count += 1
    return count

def modify_list(input_list, aDict):
    """Modify an input list if any element of this list is also inside a values of a given dictionary"""
    newList = input_list[:]
    for i in input_list:
        for j in aDict.values():
            if i in j and i in newList:
                newList.remove(i)
    return newList

def get_sum_of_dict_values(route, index):
    """Calculates the sum of parameters in route dictionary (e.g. total amount of km, euro, liter)"""
    sum = 0
    for j in route.values():
        sum += j[index]
    return round(sum, 2)

def find_shortest_route(aircraft_model, home_code, airport_list, airport_dict, aircrafts, currency_rates, currencies):
    """Function that determine the best route from a alist of airports based on the minumum distance beetween airports.
    Basically For each departure airport it will find the airport at minimum distance and selects this airport as arrival airport.
    """
    trip = 1
    takeoff_code = home_code
    km_to_do = 0
    best_route = {}
    aircraft = aircrafts.get_object_from_key(aircraft_model)

    while trip < 6:
        min_distance = sys.maxsize
        destination = home_code
        takeoff_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)

        for airp in airport_list:
            distance = airport_dict.get_distance_between_airports(takeoff_code, airp)

            if distance <= aircraft.get_range():
                """For each airport in the list if the distance to departure airport is less than aircraft range and this
                distance is the smallest among other airports, this airport will be the next destination.
                 Distance must be greater than zero, means it's not considering the departure airport as arrival airport."""
                if min_distance > distance > 0:
                    destination = airp
                    min_distance = distance

        km_to_do = airport_dict.get_distance_between_airports(takeoff_code, destination)
        fuel_needed = aircraft.get_fuel_consumed_per_km() * km_to_do
        cost_fuel = fuel_needed * takeoff_rate
        aircraft.add_fuel(fuel_needed)

        best_route[trip] = (takeoff_code, destination, km_to_do, cost_fuel, fuel_needed)
        takeoff_code = destination
        aircraft.remove_fuel_consumed(fuel_needed)

        trip += 1
        airport_list = modify_list(airport_list, best_route)
        if destination == home_code:
            break

    if len(airport_list) > 0 or km_to_do > aircraft.get_range():
        best_route = {}

    return best_route

def get_airport_at_min_distance_within_range(takeoff_code, destination, aircraft, airport_list, airport_dict):
    """Gets the airport at minimum distance from takeoof code airport considering the aircraft range"""
    min_distance = sys.maxsize
    for code in airport_list:
        code_distance = airport_dict.get_distance_between_airports(takeoff_code, code)
        if code != takeoff_code and code_distance <= aircraft.get_range() and code_distance < min_distance:
            destination = code
            min_distance = code_distance
    return destination

def find_route_with_possible_stopover(aircraft_model, home_code, airport_list, airport_dict, aircrafts, currency_rates, currencies):
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
    aircraft = aircrafts.get_object_from_key(aircraft_model)
    takeoff_code = home_code
    distance = 0
    best_route = {}
    list_stop_over = airport_list[:]  # supporting list
    trip = 1
    cheapest_rate = currency_rates.get_cheapest_rate_from_airport_codes([*airport_list, home_code], airport_dict,
                                                                            currencies)
    airport_already_twice = False

    while trip < 7:
        destination = ''
        takeoff_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
        fuel_rate = takeoff_rate

        if len(airport_list) == 0:
            airport_max = home_code
        else:
            airport_max = airport_dict.get_airport_at_max_distance(takeoff_code, airport_list)

        distance = airport_dict.get_distance_between_airports(takeoff_code, airport_max)

        if count_visited_airports(best_route, takeoff_code) >= 1:
            # Check if some airports have been visisted twice. If so modifies the list of possible stopover
            airport_already_twice = True
        if airport_already_twice:
            list_stop_over = airport_list

        best_cost = takeoff_rate * distance

        for airp in list_stop_over:
            """For each airport still in the stop over list, it checks if there is any airport between
               the departure and its farthest airport. If this airport is at the distance to each of them less
               than aircraft range and it's the most convenient then the program chooses this airport and get two trips.
                First trip - departure to selected airport and second trip - selected airport to farthest airport
            """
            if airp != takeoff_code and airp != airport_max and count_visited_airports(best_route, takeoff_code) < 1:
                distance_takeoff_airp = airport_dict.get_distance_between_airports(takeoff_code, airp)
                distance_airp_airpmax = airport_dict.get_distance_between_airports(airp, airport_max)
                airp_rate = currency_rates.get_rate_from_country(airp, airport_dict, currencies)
                if distance_airp_airpmax <= aircraft.get_range() and distance_takeoff_airp <= aircraft.get_range():
                    if takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate < best_cost:
                        destination = airp
                        best_cost = takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate
                        distance = distance_takeoff_airp

        if destination != '':
            """If destination code is equal to empty string, it means program didn't find any airport
                in the previous iteration. In this case it will check for airport at closest distance to departure
                airport otherwise it will store two trips in best_route dictionary"""
            # Set all parameters for first trip from takeoff airport to the airport in between with airport max
            fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
            cost_fuel = fuel_needed * fuel_rate
            aircraft.add_fuel(fuel_needed)
            best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
            airport_list = modify_list(airport_list, best_route)
            aircraft.remove_fuel_consumed(fuel_needed)
            trip += 1
            # Begins to set up next trip between the middle destination to airport max
            takeoff_code = destination
            if count_visited_airports(best_route, takeoff_code) >= 1:
                airport_already_twice = True
            destination = airport_max
            fuel_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
        else:
            """If the distance between farthest airport and the departure airport is less than aircraft range, then
               it checks first if the departure airport has better rate, if so next destination will be farthest airport,
               otherwise it will check for a closest airport"""
            if distance <= aircraft.get_range():
                if airport_max == home_code:
                    destination = home_code
                elif takeoff_rate <= cheapest_rate:
                    destination = airport_max
                else:
                    destination = get_airport_at_min_distance_within_range(takeoff_code, destination, aircraft,
                                                                   list_stop_over, airport_dict)
            else:
                break

        #Set parameters for nth trip and store in the route
        distance = airport_dict.get_distance_between_airports(takeoff_code, destination)
        fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
        cost_fuel = fuel_needed * fuel_rate
        aircraft.add_fuel(fuel_needed)
        best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
        aircraft.remove_fuel_consumed(fuel_needed)
        airport_list = modify_list(airport_list, best_route)
        takeoff_code = destination

        if destination == home_code:
            break
        trip += 1
    if len(airport_list) > 0 or distance > aircraft.get_range():
        """At the end of the while loop programs check if there is still some airports which hasn't been visited or
        if the last trip to the ending airport is less than aircraft range"""
        best_route = {}

    return best_route

def calculate_total_longest_distance(airport_list):
    """Calculates the sum of all the airports at the maximum distance for each airport in the list"""
    airport_dict = AirportAtlas('airport.csv')
    total_distance = 0
    for code in airport_list:
        farthest_airp = airport_dict.get_airport_at_max_distance(code, airport_list)
        total_distance += airport_dict.get_distance_between_airports(code, farthest_airp)
    return total_distance

def find_route_saving_fuel(aircraft_model, home_airport, airport_list, airport_dict, aircrafts, currency_rates, currencies):
    """This method it will find the cheapest route considering the fuel capacity of the aircraft. The primary goal is to find always the cheapest
    airport and heading towards it. After getting the cheapest airport the aircraft will be filled it up to save money when
    the route will hit a pricey airport. The algorithm considers to not fill it up to the max capacity as this will be more
    expensive in case where the route is very short. Therefore it has been calculate a longest distance that allow to fill itup
    to total maximum distance between the airports still in the list (i.e they still need to be visited)
    """
    aircraft = aircrafts.get_object_from_key(aircraft_model)
    longest_distance = calculate_total_longest_distance([*airport_list, home_airport])
    takeoff_code = home_airport
    trip = 1
    distance = 0
    best_route = {}

    while trip < 6 :
        destination = home_airport
        takeoff_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
        cheapest_airp = get_cheapest_airport_at_min_distance(takeoff_code, airport_list, airport_dict, currency_rates,
                                                             currencies)
        if len(airport_list) > 0:

            dist_takeoff_cheapest = airport_dict.get_distance_between_airports(takeoff_code, cheapest_airp)
            airp_at_max_dist = airport_dict.get_airport_at_max_distance(takeoff_code, airport_list)
            """If the departure airport is not the cheapest and the cheapest airport is not at its maximum distance, then
            the destination airport it will be the cheapest airport. Otherwise if the departure airport is the cheapest then
            the aircraft will fly to the airport at maximum distance from departure airport. Otherwise it will find any airport
            that is not at maximum distance and still in the aircraft range"""
            if takeoff_code != cheapest_airp and dist_takeoff_cheapest <= aircraft.get_range() and cheapest_airp != airp_at_max_dist:
                destination = cheapest_airp
            elif takeoff_code == cheapest_airp and dist_takeoff_cheapest <= aircraft.get_range():
                dist_takeoff_airp_max = airport_dict.get_distance_between_airports(takeoff_code, airp_at_max_dist)
                while dist_takeoff_airp_max > aircraft.get_range():
                    temp_list = [code for code in airport_list if airport_dict.get_distance_between_airports(takeoff_code, code) < dist_takeoff_airp_max]
                    if len(temp_list) > 0:
                        airp_at_max_dist = airport_dict.get_airport_at_max_distance(takeoff_code, temp_list)
                        dist_takeoff_airp_max = airport_dict.get_distance_between_airports(takeoff_code, airp_at_max_dist)
                    else:
                        break
                else:
                    destination = airp_at_max_dist
            else:
                cheapest_route = sys.maxsize
                for airp in airport_list:
                    if airp != takeoff_code and airp != airp_at_max_dist:
                        dist_airp_takeoff = airport_dict.get_distance_between_airports(takeoff_code, airp)
                        dist_airp_cheapest = airport_dict.get_distance_between_airports(airp, cheapest_airp)
                        airp_rate = currency_rates.get_rate_from_country(airp, airport_dict, currencies)
                        if dist_airp_takeoff <= aircraft.get_range() and dist_airp_cheapest <= aircraft.get_range():
                            if dist_airp_takeoff * takeoff_rate + dist_airp_cheapest * airp_rate < cheapest_route:
                                cheapest_route = dist_airp_takeoff * takeoff_rate + dist_airp_cheapest * airp_rate
                                destination = airp
                                distance = dist_airp_takeoff
                #Set parameters for first trip from departure to the airport between departure and cheapest airport
                fuel_needed = aircraft.calculate_fuel_needed(distance)
                aircraft.add_fuel(fuel_needed)
                cost_fuel = fuel_needed * takeoff_rate
                best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
                # Modify list to avoid hitting same airport twice
                airport_list = modify_list(airport_list, best_route)
                aircraft.remove_fuel_consumed(distance * aircraft.get_fuel_consumed_per_km())
                if destination == home_airport:
                    break
                # Modify longest distance considering the new list, therefore without the departure airport
                longest_distance = calculate_total_longest_distance([*airport_list, home_airport])
                takeoff_code = destination
                destination = cheapest_airp
                trip += 1

        distance = airport_dict.get_distance_between_airports(takeoff_code, destination)
        """If departure is the cheapest aiport then fill the aircraft up to the longest distance, otherwise only the necessary fuel to
        get the next airport"""
        if takeoff_code == cheapest_airp:
            fuel_needed = aircraft.calculate_fuel_needed(longest_distance)
            aircraft.add_fuel(fuel_needed)
        else:
            fuel_needed = aircraft.calculate_fuel_needed(distance)
            aircraft.add_fuel(fuel_needed)

        # Set parameters for nth trip and store data in best_route dictionary.
        cost_fuel = fuel_needed * takeoff_rate
        best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
        aircraft.remove_fuel_consumed(distance * aircraft.get_fuel_consumed_per_km())
        airport_list = modify_list(airport_list, best_route)
        longest_distance = calculate_total_longest_distance([*airport_list, home_airport])
        takeoff_code = destination
        trip += 1
        if destination == home_airport:
            break
    if distance > aircraft.get_range() or len(airport_list) > 0:
        #If after searching the route there is still any airport that has not been visited, or the distance last airport
        #  go back home is greater than maximum aircraft range then delete route found as it's not valuable
        best_route = {}
    return best_route

def get_cheapest_airport_at_min_distance(home_airport, airport_list, airport_dict, currency_rates, currencies):
     airport_list = [*airport_list, home_airport]
     cheapest_rate = currency_rates.get_cheapest_rate_from_airport_codes(airport_list, airport_dict,
                                                                        currencies)
     list_cheapest = []
     for airp in airport_list:
         if currency_rates.get_rate_from_country(airp, airport_dict, currencies) == cheapest_rate:
             list_cheapest.append(airp)
     if len(list_cheapest) == 1:
        return list_cheapest[0]
     else:
        return airport_dict.get_airport_at_min_distance(home_airport, list_cheapest)

def find_cheapest_route(aircraft_model, home_code, airport_list, aircrafts, airport_dict):
    """Gathers the three find route methods and it will find the cheapest route for the selected list of airports.
    This is the main method which it will run on GUI"""
    list_routes = []
    currency_rates = CurrencyRatesDictionaryParent('currencyrates.csv')
    currencies = CountryCurrenciesDictionaryParent('countrycurrency.csv')
    list_routes.append(find_route_with_possible_stopover(aircraft_model, home_code, airport_list, airport_dict,
                                                         aircrafts, currency_rates, currencies))

    list_routes.append(find_shortest_route(aircraft_model, home_code, airport_list, airport_dict, aircrafts,
                                            currency_rates, currencies))
    list_routes.append(find_route_saving_fuel(aircraft_model, home_code, airport_list, airport_dict,
                                              aircrafts, currency_rates, currencies))
    best_price = sys.maxsize
    best_route = {}
    for i in list_routes:
        if 0 != get_sum_of_dict_values(i, 3) < best_price:
            best_price = get_sum_of_dict_values(i, 3)
            best_route = i
    if best_route == {}:
        raise RouteNotFoundError('Sorry. No route found for this aircraft to the selected destinations.')

    return get_info_best_route(airport_dict, best_route)

def get_info_best_route(airport_dict, route_dict):
    """Method to display information of the various airport in the route"""
    output_route = {}
    for trip, route in route_dict.items():
        dep_airp = airport_dict.get_object_from_key(route[0]).__str__()
        arr_airp = airport_dict.get_object_from_key(route[1]).__str__()
        cost = round(route[3], 2)
        fuel = round(route[4], 2)
        output_route[trip] = (dep_airp, arr_airp, route[2], cost, fuel)
    return output_route
