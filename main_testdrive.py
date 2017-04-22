from airport_atlas import AirportAtlas
from airport import Airport
from aircraft import Aircraft
from country_currencies import CountryCurrenciesDictionary
from currency_rates import CurrencyRatesDictionary
from aircrafts_dictionary import AircraftDictionary
from best_routes import get_sum_of_dict_values,find_shortest_route,find_route_with_possible_stopover, \
    find_cheapest_route, find_route_with_possible_stopover_modif


def main():
    atl = AirportAtlas('airport.csv')
    # print(atl.get_airport_at_max_distance('JFK', ['DUB', 'ZAZ', 'JFK', 'CDG']))
    # print(atl.get_distance_between_airports('JFK', 'CDG'))
    # print(atl.get_distance_between_airports('JFK', 'ZAZ'))
    # print(atl.get_distance_between_airports('ZAZ', 'CDG'))
    # route = best_route_for_aircraft('A319', 'DUB', ['KBL', 'MMY', 'MOW', 'LHR'])
    # route6 = best_route_for_aircraft('A319', 'KBL', ['DUB', 'MMY', 'MOW', 'LHR'])
    #print( best_route_for_aircraft('777', 'MMY', ['KBL', 'DUB', 'MOW', 'LHR']))
    #print(best_of_all_routes('777', 'LHR', ['DUB', 'CDG', 'JFK', 'AAL']))
    #print(best_of_all_routes('777', 'DUB', ['LHR', 'CDG', 'JFK', 'AAL']))
    #route3 = best_route_for_aircraft('A319', 'MOW', ['KBL', 'MMY', 'DUB', 'LHR'])
    # route4 = best_route_for_aircraft('A319', 'LHR', ['KBL', 'MMY', 'MOW', 'DUB'])
    # route2 = best_route_for_aircraft_version_2('A319', 'LHR', ['KBL', 'MMY', 'MOW', 'DUB'])
    # route5 = best_route_cheapest_destination('A319', 'LHR', ['KBL', 'MMY', 'MOW', 'DUB'])
    # route7 = route_min_distance('A319', 'LHR', ['KBL', 'MMY', 'MOW', 'DUB'])
    #print(best_of_all_routes('F50', 'DUB', ['LHR', 'CDG', 'JFK', 'AAL']))
    #print(best_of_all_routes('A319', 'DUB', ['BPE', 'ELV', 'LRV', 'INN']))
    #
    #
    # route1 = best_route_cheapest_destination('A319', 'DUB', ['KBL', 'ZAZ', 'PBD', 'YQT'])
    # route6 = best_route_for_aircraft_version_2('A319', 'DUB', ['KBL', 'ZAZ', 'PBD', 'YQT'])
    #print(find_cheapest_route('A319', 'DUB', ['KBL', 'ZAZ', 'PBD', 'YQT']))
   #  print(find_route_with_possible_stopover_modif('A319', 'DUB', ['KBL', 'ZAZ', 'PBD', 'YQT']))
   #  # # route8 = route_min_distance('A319', 'DUB', ['KBL', 'ZAZ', 'PBD', 'YQT'])
   #  # print(best_route_for_aircraft('A319', 'DUB', ['lhr', 'ZAZ', 'PBD', 'YQT']))
   #  # print(best_route_for_aircraft('A319', 'DUB', ['lhr', 'ZAZ', 'PBD', 'YQT']))
   #  #print(best_route_for_aircraft('777', 'DUB', ['lhr', 'ZAZ', 'PBD', 'YQT']))
   #  # route4 = best_route_for_aircraft('A319', 'PKK', ['KBL', 'THR', 'PBD', 'LHR'])
   #  # route6 = best_route_for_aircraft('A319', 'PKK', ['KBL', 'THR', 'PBD', 'LHR'])
   # # print(best_of_all_routes('777', 'PKK', ['KBL', 'THR', 'PBD', 'LHR']))
   #  print(find_route_with_possible_stopover('747-200', 'BIN', ['TIA', 'BST', 'ALG', 'LWN'],AirportAtlas('airport.csv'), AircraftDictionary('aircraft.csv'),
   #                                        CurrencyRatesDictionary('currencyrates.csv'), CountryCurrenciesDictionary('countrycurrency.csv')))
   #  print(find_shortest_route('747-200', 'BIN', ['TIA', 'BST', 'ALG', 'LWN']))
   #  print(best_route_for_aircraft_version_2('737-600', 'BIN', ['TIA', 'AZ3', 'BST', 'LWN']))
    print(find_cheapest_route('737-600', 'TIA', ['ALG', 'OFU', 'BBQ', 'BHI'], AircraftDictionary('aircraft.csv'),AirportAtlas('airport.csv')))

    # print(find_route_with_possible_stopover('C212', 'LHR', ['DUB', 'ZAZ', 'JFK', 'CDG'], AirportAtlas('airport.csv'),
    #                           AircraftDictionary('aircraft.csv'), CurrencyRatesDictionary('currencyrates.csv'),
    #                           CountryCurrenciesDictionary('countrycurrency.csv')))
    # print(
    #     find_route_with_possible_stopover_modif('737-600', 'BIN', ['TIA', 'AZ3', 'BST', 'LWN']))
    #print(find_route_with_possible_stopover_modif('777', 'MMY', ['KBL', 'DUB', 'MOW', 'LHR']))
    #print(ret_sum(best_route_for_aircraft('777', 'PKK', ['KBL', 'THR', 'PBD', 'LHR']),3))print(
    #print(find_cheapest_route('777', 'MMY', ['KBL', 'DUB', 'MOW', 'LHR'],  AircraftDictionary('aircraft.csv'), AirportAtlas('airport.csv')))

    #print(best_of_all_routes('777', 'DUB', ['lhr', 'ZAZ', 'PBD', 'YQT']))
    #print(best_of_all_routes('777', 'LHR', ['KBL', 'MMY', 'MOW', 'DUB']))
    #print(best_of_all_routes('A319', 'DUB', ['KBL', 'ZAZ', 'PBD', 'YQT']))
    #print(best_of_all_routes('777', 'MMY', ['KBL', 'DUB', 'MOW', 'LHR']))
    #print(best_route_for_aircraft('777', 'MMY', ['KBL', 'DUB', 'MOW', 'LHR']))
    #print(ret_sum(best_route_for_aircraft('777', 'MMY', ['KBL', 'DUB', 'MOW', 'LHR']),3))

    # print(route4)
    # print('km ', ret_sum(route4, 2))
    # print('€ ',ret_sum(route4, 3))
    # print(route2)
    # print('km ', ret_sum(route2, 2))
    # print('€ ', ret_sum(route2, 3))
    # print(route5)
    # print('km ', ret_sum(route5, 2))
    # print('€ ', ret_sum(route5, 3))
    # print(route7)
    # print('km ', ret_sum(route7, 2))
    # print('€ ', ret_sum(route7, 3))
    # print()
    # print(route1)
    # print('km ', ret_sum(route1, 2))
    # print('€ ', ret_sum(route1, 3))
    # print(route6)
    # print('km ', ret_sum(route6, 2))
    # print('€ ', ret_sum(route6, 3))
    # print(route3)
    # print('km ', ret_sum(route3, 2))
    # print('l ', ret_sum(route3, 3))
    # print(route8)
    # print('km ', ret_sum(route8, 2))
    # print('€ ', ret_sum(route8, 3))


if __name__ == "__main__":
    main()
