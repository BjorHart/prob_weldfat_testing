import numpy as np
import theano
import theano.tensor as tt
import pymc3 as pm
import matplotlib.pyplot as plt
from theano.ifelse import ifelse
from math import sin, cos
import json
""" Input json to be imported to prob_weldfat """

def input():
    time = [4.0 * i / 200 for i in range(200 + 1)]
    series = np.array([0.2 + 0.5 * sin(t) + 0.2 * cos(10*t) + 0.2 * sin(4*t) for t in time])*1e2
    series = list(series)
    input_serie_2 = {}
    input_serie_2['method'] = 'Nominal Fatigue' 
    input_serie_2['fatigue_class'] = {
        'fat':100, # ["normal",100.0,10],
        'fatFact': 1.0,
        'n_fat': ["normal",2000000.0,1000],
        'n_c': 10000000.0,
        'm_1': 5,#["normal",5.0,1],
        'm_2': 22.0,
        }
    input_serie_2['stress_unit'] = 'MPa'
    input_serie_2['serie_data'] = {'series': series}
    input_serie_2['mean_stress_theory'] = {'theory': 'Goodman',
            'ultimate_limit': 500.}
    return json.dumps(input_serie_2)
