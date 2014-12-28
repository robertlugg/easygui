__author__ = 'Robert'

"""
Sample application using new API to display weather conditions
"""

import requests
from pprint import pprint
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Portland,ME,US')
pprint(r.json())