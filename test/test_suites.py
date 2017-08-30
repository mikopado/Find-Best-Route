from test.test_airportAtlas import *
from test.test_route_algorithms import *

from test.test_currency_rates import *


def alltests():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(TestAirportAtlas))
    tests.addTest(unittest.makeSuite(TestCurrencyRates))
    tests.addTest(unittest.makeSuite(TestRouteAlgorithms))
    return tests

runner = unittest.TextTestRunner()
runner.run(alltests())