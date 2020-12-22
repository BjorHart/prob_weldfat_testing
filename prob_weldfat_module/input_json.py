import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos
import json

""" Input json to be imported to prob_weldfat """

time_ = [4.0 * i / 200 for i in range(200 + 1)]
series = np.array([0.2 + 0.5 * sin(t) + 0.2 * cos(10*t) + 0.2 * sin(4*t) for t in time_])*1e2
series = list(series)

input_json = {}
input_json['method'] = 'Nominal Fatigue' 
input_json['fatigue_class'] = {
    'fat':100,#["normal",100.0,10], #//  dnvgl = 100, tests = 95,93,88
    'fatFact': 1, #["uniform",1,2],
    'n_fat': 2e6, #["normal",2e6,100000], 
    'n_c': 1e7, #["normal",10000000.0,1000000],
    'm_1': {"d":"normal","m":10,"sd":1}, #["normal",5.0,1],
    'm_2': 100, #["normal",22.0,1]
    }
#input_json['stress_data'] = {'rng': 1, 'cycles': 1}
input_json['stress_unit'] = 'MPa'
input_json['serie_data'] = {'series': series}
input_json['mean_stress_theory'] = {'theory': 'Soderberg',
        'yield_limit': {"d":"normal","m":500.,"sd":10}}
input_json = json.dumps(input_json,indent=4,sort_keys=True)

print(input_json)