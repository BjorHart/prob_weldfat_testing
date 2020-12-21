import requests
import json
from math import sin, cos

# Creating moc data

time = [4.0 * i / 200 for i in range(200 + 1)]
series = [0.2 + 0.5 * sin(t) + 0.2 * cos(10*t) + 0.2 * sin(4*t) for t in time]

input_serie_1 = {}
input_serie_1['method'] = 'Nominal Fatigue'
input_serie_1['fatigue_class'] = {'class': 'IIW FAT125 steel'}
input_serie_1['stress_unit'] = 'MPa'
input_serie_1['serie_data'] = {'series': series}
input_json = json.dumps(input_serie_1)