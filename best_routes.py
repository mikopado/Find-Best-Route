import sys
from airport_atlas import AirportAtlas
from currency_rates import CurrencyRatesDictionary
from country_currencies import CountryCurrenciesDictionary
from aircrafts_dictionary import AircraftDictionary
from custom_exceptions import *


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
        aircraft.add_fuel(km_to_do)

        best_route[trip] = (takeoff_code, destination, km_to_do, cost_fuel, fuel_needed)
        takeoff_code = destination
        aircraft.remove_fuel_consumed(km_to_do)

        trip += 1
        airport_list = modify_list(airport_list, best_route)
        if destination == home_code:
            break

    if len(airport_list) > 0 or km_to_do > aircraft.get_range():
        best_route = {}

    return best_route


def find_route_with_possible_stopover(aircraft_model, home_code, airport_list, airport_dict, aircrafts, currency_rates,
                                      currencies):
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
    the aircraft range, it will check if there is any airport beetween them at distance less than aircraft range and at
    convenient rate. If it finds this airport the algorithm already has identified two trips. If it doesn't find any airport
    in beetween to split the largest distance, it will find an airport at minimum distance.
    If the distance beetween departure airport to its furthest airport is less than aircraft range, it will check first of all
    if the currency rate at departure airport is cheaper than arrival airport, in this case arrival airport it will be
    equal to the furthest airport. Otherwise it will find the airport at minimum distance
    """
    aircraft = aircrafts.get_object_from_key(aircraft_model)
    takeoff_code = home_code
    distance = 0
    best_route = {}
    list_stop_over = airport_list[:]  # supporting list
    trip = 1
    cheapest_rate = currency_rates.get_cheapest_rate_from_airport_codes([*airport_list, home_code], airport_dict, currencies)
    airport_already_twice = False
    while trip < 7:
        destination = home_code
        takeoff_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
        fuel_rate = takeoff_rate

        if len(airport_list) > 0:

            airport_max = airport_dict.get_airport_at_max_distance(takeoff_code, airport_list)
            distance = airport_dict.get_distance_between_airports(takeoff_code, airport_max)
            best_cost = takeoff_rate * airport_dict.get_distance_between_airports(takeoff_code, airport_max)

            if count_visited_airports(best_route, takeoff_code) >= 1:
                # Check if some airports have been visisted twice. If so modifies the list of possible stopover
                #list_stop_over = modify_list(list_stop_over, best_route)
                airport_already_twice = True
            if airport_already_twice:
                list_stop_over = airport_list
            for airp in list_stop_over:
                """For each airport still in the stop over list, it checks if there is any airport beetween
                the departure and its farthest airport. If this airport is at the distance to each of them less
                than aircraft range and it's the most convenient then the program chooses this airport and get two trips.
                 First trip - departure to selected airport and second trip - selected airport to farthest airport
                 """
                if airp != takeoff_code and airp != airport_max:
                    distance_takeoff_airp = airport_dict.get_distance_between_airports(takeoff_code, airp)
                    distance_airp_airpmax = airport_dict.get_distance_between_airports(airp, airport_max)
                    airp_rate = currency_rates.get_rate_from_country(airp, airport_dict, currencies)
                    if distance_airp_airpmax <= aircraft.get_range() and distance_takeoff_airp <= aircraft.get_range():
                        if takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate < best_cost:
                            destination = airp
                            best_cost = takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate
                            distance = distance_takeoff_airp

            if destination != home_code:
                """If destination code is equal to starting airport code, it means program didn't find any airport
                 in the previous iteration. In this case it will check for airport at closest distance to departure
                 airport otherwise it will store two trips in best_route dictionary"""

                # Set all parameters for first trip from takeoff airport to the airport in beetween with airport max
                fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
                cost_fuel = fuel_needed * fuel_rate
                aircraft.add_fuel(distance)
                best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
                aircraft.remove_fuel_consumed(distance)



                # Begins to set up next trip beetween the middle destination to airport max
                takeoff_code = destination
                destination = airport_max
                fuel_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
                if count_visited_airports(best_route, takeoff_code) >= 1:
                    airport_already_twice = True
                trip += 1

            else:
                """If the distance beetween farhest airport and the departure airport is less than aircraft range, then
                   it checks first if the departure airport has better rate, if so next destination will be farthest airport,
                   otherwise it will check for a closest airport"""
                if distance <= aircraft.get_range():
                    # if count_visited_airports(best_route, takeoff_code) >= 1:
                    #     list_stop_over = modify_list(list_stop_over, best_route)
                    if takeoff_rate <= cheapest_rate:
                        destination = airport_max
                    else:
                        destination = get_airport_at_min_distance_within_range(takeoff_code, destination, aircraft,
                                                                               list_stop_over, airport_dict)

        distance = airport_dict.get_distance_between_airports(takeoff_code, destination)
        fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
        cost_fuel = fuel_needed * fuel_rate

        aircraft.add_fuel(distance)
        best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
        aircraft.remove_fuel_consumed(distance)

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


def get_airport_at_min_distance_within_range(takeoff_code, destination, aircraft, airport_list, airport_dict):
    min_distance = sys.maxsize
    for code in airport_list:
        code_distance = airport_dict.get_distance_between_airports(takeoff_code, code)
        if code != takeoff_code and code_distance <= aircraft.get_range() and code_distance < min_distance:
            destination = code
            min_distance = code_distance
    return destination


# def best_route_for_aircraft_version_2(aircraft_model, home_code, airport_list):
#
#     airport_dict = AirportAtlas('airport.csv')
#     aircraft = AircraftDictionary('aircraft.csv').get_object_from_key(aircraft_model)
#     currency_rates = CurrencyRatesDictionary('currencyrates.csv')
#     currencies = CountryCurrenciesDictionary('countrycurrency.csv')
#     takeoff_code = home_code
#     distance = 0
#     best_route = {}
#     list_stop_over = airport_list[:]  # supporting list
#     trip = 1
#     cheapest_rate = currency_rates.get_cheapest_rate_from_airport_codes([*airport_list, home_code], airport_dict,
#                                                                         currencies)
#     highest_rate = currency_rates.get_highest_rate_from_airport_codes([*airport_list, home_code], airport_dict,
#                                                                       currencies)
#     home_rate = currency_rates.get_rate_from_country(home_code, airport_dict, currencies)
#
#     while trip < 7:
#         destination = home_code
#         takeoff_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
#         fuel_rate = takeoff_rate
#
#         if len(airport_list) >= 0:
#             if len(airport_list) == 0:
#                 airport_max = home_code
#             else:
#                 airport_max = airport_dict.get_airport_at_max_distance(takeoff_code, airport_list)
#             distance = airport_dict.get_distance_between_airports(takeoff_code, airport_max)
#
#             if distance > aircraft.get_range() and (trip != 1 or home_rate != highest_rate):
#                 """Apply this condition only if the distance beetween departure airport and the airport at maximum distance
#                     is higher than aircraft range and the starting airport is no the highest currency rate. Only for the
#                     first trip it avoids to go to furthest place if the currency rate of departure airport is the highest
#                     and so put less fuel"""
#                 best_cost = sys.maxsize
#                 if count_visited_airports(best_route, takeoff_code) >= 1:
#                     # Check if some airports have been visisted twice. If so modifies the list of possible stopover
#                     list_stop_over = modify_list(list_stop_over, best_route)
#                 for airp in list_stop_over:
#                     """For each in airport still in the stop over list, it checks if there is any airport beetween
#                     the departure and its farthest airport. If this airport is at the distance to each of them less
#                     than aircraft range and it's the most convenient. The program chooses this airport and get two trips.
#                      One departure - selected airport and second selected airport to fathest airport
#                      """
#                     distance_takeoff_airp = airport_dict.get_distance_between_airports(takeoff_code, airp)
#                     distance_airp_airpmax = airport_dict.get_distance_between_airports(airp, airport_max)
#                     airp_rate = currency_rates.get_rate_from_country(airp, airport_dict, currencies)
#                     if distance_airp_airpmax <= aircraft.get_range() and distance_takeoff_airp <= aircraft.get_range():
#                         if takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate < best_cost:
#                             destination = airp
#                             best_cost = takeoff_rate * distance_takeoff_airp + distance_airp_airpmax * airp_rate
#                             distance = distance_takeoff_airp
#
#                 if destination != home_code:
#                     """If destination code is equal to starting airport code, it means program didn't find any airport
#                     in the previous iteration. In this case it will check for airport at closest distance to departure
#                     airport otherwise it will store the two identified trips in best_route dictionary"""
#                     fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
#                     cost_fuel = fuel_needed * fuel_rate
#
#                     aircraft.add_fuel(distance)
#                     best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
#                     if count_visited_airports(best_route, takeoff_code) >= 1:
#                         list_stop_over = modify_list(list_stop_over, best_route)
#                     aircraft.remove_fuel_consumed(distance)
#                     trip += 1
#
#                     takeoff_code = destination
#                     destination = airport_max
#                     fuel_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)
#
#                 # else:
#                 #     destination = get_airport_at_min_distance(takeoff_code, destination, aircraft, list_stop_over,
#                 #                                               airport_dict)
#
#
#             else:
#                 """If the distance beetween farhest airport and the departure airport is less than aircraft range, then
#                 it checks first if the departure airport has better rate, if so next destination will be farthest airport,
#                 otherwise it will check for a closest aiport"""
#                 if count_visited_airports(best_route, takeoff_code) >= 1:
#                     list_stop_over = modify_list(list_stop_over, best_route)
#                 if takeoff_rate <= cheapest_rate:
#                     destination = airport_max
#
#             if destination == home_code:
#                 destination = get_airport_at_min_distance_within_range(takeoff_code, destination, aircraft,
#                                                                    list_stop_over, airport_dict)
#
#         distance = airport_dict.get_distance_between_airports(takeoff_code, destination)
#         fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
#         cost_fuel = fuel_needed * fuel_rate
#         aircraft.add_fuel(distance)
#         best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
#         aircraft.remove_fuel_consumed(distance)
#
#         airport_list = modify_list(airport_list, best_route)
#         takeoff_code = destination
#         if destination == home_code:
#             break
#
#         trip += 1
#     if len(airport_list) > 0 or distance > aircraft.get_range():
#         """At the end of the while loop programs check if there is still some airports which hasn't been visited or
#         if the last trip to the ending airport is less than aircraft range"""
#         #print('No best route found for all airports', list_stop_over)
#         best_route = {}
#
#     return best_route


def find_route_with_possible_stopover_modif(aircraft_model, home_code, airport_list):
    airport_dict = AirportAtlas('airport.csv')
    aircraft = AircraftDictionary('aircraft.csv').get_object_from_key(aircraft_model)
    currency_rates = CurrencyRatesDictionary('currencyrates.csv')
    currencies = CountryCurrenciesDictionary('countrycurrency.csv')
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

        if count_visited_airports(best_route, takeoff_code) >= 1:
            airport_already_twice = True
        distance = airport_dict.get_distance_between_airports(takeoff_code, airport_max)

        best_cost = takeoff_rate * distance
        if airport_already_twice:
            list_stop_over = airport_list

        for airp in list_stop_over:
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
            fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
            cost_fuel = fuel_needed * fuel_rate

            aircraft.add_fuel(distance)

            best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)

            airport_list = modify_list(airport_list, best_route)
            aircraft.remove_fuel_consumed(distance)
            trip += 1

            takeoff_code = destination
            if count_visited_airports(best_route, takeoff_code) >= 1:
                airport_already_twice = True
            destination = airport_max
            fuel_rate = currency_rates.get_rate_from_country(takeoff_code, airport_dict, currencies)

        else:
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

        distance = airport_dict.get_distance_between_airports(takeoff_code, destination)
        fuel_needed = distance * aircraft.get_fuel_consumed_per_km()
        cost_fuel = fuel_needed * fuel_rate

        aircraft.add_fuel(distance)

        best_route[trip] = (takeoff_code, destination, distance, cost_fuel, fuel_needed)
        aircraft.remove_fuel_consumed(distance)

        airport_list = modify_list(airport_list, best_route)
        takeoff_code = destination

        if destination == home_code:
            break

        trip += 1
    if len(airport_list) > 0 or distance > aircraft.get_range():
            # print('No best route found for all airports', list_stop_over)
        best_route = {}

    return best_route

def find_cheapest_route(aircraft_model, home_code, airport_list, aircrafts, airport_dict):
    list_routes = []
    currency_rates = CurrencyRatesDictionary('currencyrates.csv')
    currencies = CountryCurrenciesDictionary('countrycurrency.csv')
    list_routes.append(find_route_with_possible_stopover(aircraft_model, home_code, airport_list, airport_dict,
                                                         aircrafts, currency_rates, currencies))

    list_routes.append(find_shortest_route(aircraft_model, home_code, airport_list, airport_dict, aircrafts,
                                            currency_rates, currencies))
    list_routes.append(find_route_with_possible_stopover_modif(aircraft_model,home_code,airport_list))
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
    output_route = {}
    for trip, route in route_dict.items():
        dep_airp = airport_dict.get_object_from_key(route[0]).__str__()
        arr_airp = airport_dict.get_object_from_key(route[1]).__str__()
        cost = round(route[3], 2)
        fuel = round(route[4], 2)
        output_route[trip] = (dep_airp, arr_airp, route[2], cost, fuel)
    return output_route
