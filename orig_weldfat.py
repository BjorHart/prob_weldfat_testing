import json
import datetime
from collections import deque, defaultdict
import rainflow
from WeldFat_Pref import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
import time

""" original weldfat code for comparison with probabilistic weldfat results"""


time_ = [4.0 * i / 200 for i in range(200 + 1)]
series = np.array([0.2 + 0.5 * sin(t) + 0.2 * cos(10*t) + 0.2 * sin(4*t) for t in time_])*1e2
series = list(series)
input_serie_2 = {}
input_serie_2['method'] = 'Nominal Fatigue' 
input_serie_2['fatigue_class'] = {
    'fat': 100,#["normal",100.0,10],
    'fatFact': 1.0,
    'n_fat': 2000000, #["normal",2000000.0,10],
    'n_c': 10000000.0,
    'm_1': 5.0,
    'm_2': 22.0,
    }
input_serie_2['stress_unit'] = 'MPa'
input_serie_2['serie_data'] = {'series': series}
input_serie_2['mean_stress_theory'] = {'theory': 'Goodman',
        'ultimate_limit': 500.}
json_input = json.dumps(input_serie_2)
timestamp=1
_componentId="aaa"
response=[""]

fat = np.random.normal(100,10,size=1000)

def WeldFat(timestamp, _componentId, json_input,response):
    """Iterate cycles in the series.

    Parameters
    ----------
    timestamp (datetime.datetime): 
    _componentId (string): "e9fafc85-5f4d-422e-8988-6545890f202c"
    jsonjson_obj (string):  
    Returns
    ------
    res_dict dictionary as json
    
    res_dict['cumulative_damage']
    res_dict['safety_factor_life_per_bin']
    res_dict['equivalent_stress_range']
    res_dict['safety_factor_stress']
    res_dict['rst'] : Fatigue result per bin as below
        res_dict['rst'][bin]['life']
        res_dict['rst'][bin]['log10_life']
        res_dict['rst'][bin]['damage_per_bin']
        res_dict['rst'][bin]['safety_factor_life_per_bin']
        
    """

    # read json json_objs

    json_obj = {}
    json_obj = json.loads(json_input)

    # Define unit conversion from user units to stress_unit_dict units

    #stress_unit = json_obj['stress_unit']
    stress_unit_dict = {'mpa': 1.0, 'psi': 145.038, 'ksi': 0.145038} #Mpa to user unit
    #conv_stress = stress_unit_dict[stress_unit.lower()] #convert MPa to user unit

    # Get S-N Curve definition parameters

    if 'class' not in json_obj['fatigue_class']:
        fat_class = 'User defined'
        fat = json_obj['fatigue_class']['fat'] 
        n_fat = json_obj['fatigue_class']['n_fat']
        n_c = json_obj['fatigue_class']['n_c']
        m_1 = json_obj['fatigue_class']['m_1']
        m_2 = json_obj['fatigue_class']['m_2']
    else:
        fat_class = json_obj['fatigue_class']['class']
        if fat_class in fatClassDict:
            fat = fatClassDict[fat_class]['FAT'][0] * stress_unit_dict[fatClassDict[fat_class]['FAT'][1].lower()]#SN curve in MPa change to user unit
            n_fat = fatClassDict[fat_class]['Nfat']
            n_c = fatClassDict[fat_class]['Nc']
            m_1 = fatClassDict[fat_class]['m1']
            m_2 = fatClassDict[fat_class]['m2']
        else:
            response[0] = fat_class + ' not found in fatClassDict - not catch json schema validator'
    
    if 'fat_fact' not in json_obj['fatigue_class']:
        fat_fact = 1.
    else:
        fat_fact = json_obj['fatigue_class']['fat_fact']

    if 'N0' in fatClassDict[fat_class]:
        n_0 = fatClassDict[fat_class]['N0']
    else:
        n_0 = 1

    if 'm0' in fatClassDict[fat_class]:
        m_0 = fatClassDict[fat_class]['m0']
    else:
        m_0 = 1

    if 'Ncutoff' in fatClassDict[fat_class]:
        n_cutoff = fatClassDict[fat_class]['Ncutoff']
    else:
        n_cutoff = 1
    
    res_dict = {}
    
    res_dict['stress_unit']=json_obj['stress_unit']
    # Save SN parameters for user check
    
    res_dict['sn_parameters']={}
    res_dict['sn_parameters']['class']=fat_class
    res_dict['sn_parameters']['fat']=fat
    res_dict['sn_parameters']['n_fat']=n_fat
    res_dict['sn_parameters']['n_c']=n_c
    res_dict['sn_parameters']['m_1']=m_1
    res_dict['sn_parameters']['m_2']=m_2
    res_dict['sn_parameters']['fat_fact']=fat_fact
    res_dict['sn_parameters']['n_0']=n_0
    res_dict['sn_parameters']['m_0']=m_0
    res_dict['sn_parameters']['n_cutoff']=n_cutoff
    
    # intermediate parameters

    log10_sn_1 = log10(fat * fat_fact) + (log10(n_fat) - log10(n_0)) / m_1
    sn_1 = 10 ** log10_sn_1
    sn_0 = 10 ** (log10_sn_1 + log10(n_0) / m_0)
    sn_c = 10 ** (log10(fat * fat_fact) - (log10(n_c) - log10(n_fat)) / m_1)

    # added extraction of sn_cutoff to plot curve
    sn_cutoff = 10 ** (log10(sn_c) - (log10(n_cutoff)-log10(n_c))/m_2)
   
   #plot sn-curve
    sn_s = [sn_1,sn_0,sn_c,sn_cutoff]
    log_sn_s = [log10(s) for s in sn_s]
    n_s = [n_0,n_0,n_c,n_cutoff]
    log_n_s = [log10(n) for n in n_s]
    plt.plot(log_n_s,log_sn_s)
    plt.savefig("deterministic_SN_curve")
    plt.close()

    # Get mean stress theory parameter
    if 'mean_stress_theory' in json_obj:
        mean_stress_theory = json_obj['mean_stress_theory']['theory']
        if mean_stress_theory in ['Goodman', 'Gerber']:
            r_m = json_obj['mean_stress_theory']['ultimate_limit']
            r_y = 0.9 * r_m
        elif mean_stress_theory == 'Soderberg':
            r_m = 0.
            r_y = json_obj['mean_stress_theory']['yield_limit']
        else:
            response[0] = mean_stress_theory + ' not found in mean_stress_theory - not catch json schema validator'

    # Calculate result per bin

    #res_dict = {}
    res_dict['cumulative_damage'] = 0.
    res_dict['safety_factor_life_per_bin'] = 0.
    res_dict['equivalent_stress_range'] = 0.
    res_dict['safety_factor_stress'] = 0.
    res_dict['result_per_bin'] = {}

    # rainflow counting in the user unit

    if 'stress_data' not in json_obj.keys() and 'serie_data' in json_obj.keys():
        series = json_obj['serie_data']['series']
        if series ==[]:
            response[0] = 'serie '+str(series)+' not valid'
            return
        if 'nbins' in json_obj['serie_data'].keys():
        
            max_range = max(series) - min(series)
            if 'maxrange' in json_obj['serie_data']:
                my_max_range = json_obj['serie_data']['maxrange']
                max_range = my_max_range
                if max_range < my_max_range:  
                    pass
                else:
                    response[0] = 'Warning: serie max range larger than given max range'
                    
            nbins = json_obj['serie_data']['nbins']
            binsize = max_range / nbins
            
            counts_ix = defaultdict(int)
            for i in range(nbins):
                counts_ix[i] = 0

            # Apply mean stress theory before assigning to bin

            for (rng, mean, count, i_start, i_end) in rainflow.extract_cycles(series):
            
                if 'mean_stress_theory' in json_obj:
                    sn_0_user_unit= sn_0
                    rng = apply_mean_stress_theory(mean_stress_theory,mean,rng,sn_0_user_unit,r_m,r_y)
                bin_index = int(abs(rng) / binsize)

                # handle possibility of range equaliing max range

                if bin_index == nbins:
                    bin_index = nbins - 1
                counts_ix[bin_index] += count

            # save count data to dictionary where key is the range

            counts = dict(((k + 1) * binsize, v) for (k, v) in counts_ix.items())
            cycles_list = sorted(counts.items())

            json_obj['stress_data'] = {}
            
            for i in range(len(cycles_list)):
                json_obj['stress_data'][i] = {'rng': cycles_list[i][0], 'cycles': cycles_list[i][1], 'sm': 0.}
            if 'mean_stress_theory' in json_obj:
                del json_obj['mean_stress_theory']
        elif 'maxrange' in json_obj['serie_data'].keys() and not 'nbins' in json_obj['serie_data'].keys():
            response[0] = '"maxrange" and no "nbins" not currently handle - not catch json schema validator'
        else:
            json_obj['stress_data'] = {}
            for (i, (rng, mean, count, i_start, i_end)) in enumerate(rainflow.extract_cycles(series)):
                json_obj['stress_data'][i] = {'rng': rng, 'cycles': count, 'sm': mean}

        #res_dict['stress_data'] = json_obj['stress_data']
    
    # Fatigue calculation in MPa unit
    it=0
    for bin in json_obj['stress_data'].keys():
        if it==0:
            cycles = json_obj['stress_data'][bin]['cycles']
            rng = json_obj['stress_data'][bin]['rng'] 
            if 'sm' in json_obj['stress_data'][bin]:
                sm = json_obj['stress_data'][bin]['sm'] 
            else:
                sm = 0.

            # init result dictionary

            _rst_dic_per_bin = {}
            _rst_dic_per_bin['rng'] = rng
            _rst_dic_per_bin['mean'] = sm
            _rst_dic_per_bin['corrected_rng'] = rng
            _rst_dic_per_bin['cycles'] = cycles
            _rst_dic_per_bin['life'] = 0.
            _rst_dic_per_bin['log10_life'] = 0.
            _rst_dic_per_bin['damage_per_bin'] = 0.
            _rst_dic_per_bin['safety_factor_life_per_bin'] = 0.    

            if cycles != 0.:

                # calculate s_nb

                if cycles <= n_0:
                    s_nb = 10 ** (log10_sn_1 + (log10(n_0) - log10(cycles))/ m_0)
                elif cycles <= n_c:
                    s_nb = 10 ** (log10(sn_c) + (log10(n_c) - log10(cycles)) / m_1)
                else:
                    s_nb = 10 ** (log10(sn_c) - (log10(cycles) - log10(n_c)) / m_2)
                                
                # mean stress theory

                if 'mean_stress_theory' in json_obj and 'sm' in json_obj['stress_data'][bin]:
                    if rng > 1.5*r_y: 
                        response[0] = 'The calculated Nominal stress range exceeds the 1.5*Yield Stress for the material.  The fatigue calculations may not be valid.  Please check the results carefully.'
                    if json_obj['stress_data'][bin]['sm'] != 0.:            
                        mean_stress_theory = json_obj['mean_stress_theory']['theory']
                        rng = apply_mean_stress_theory(mean_stress_theory,sm,rng,sn_0,r_m,r_y)
                        _rst_dic_per_bin['corrected_rng']=rng
                    else:
                        _rst_dic_per_bin['corrected_rng'] = rng
                else :
                    _rst_dic_per_bin['corrected_rng'] = rng

            # Calculate life and store result

            if rng > sn_0:
                _rst_dic_per_bin['log10_life'] = -1.
                _rst_dic_per_bin['life'] = 0.
                _rst_dic_per_bin['damage_per_bin'] = 100.0
                _rst_dic_per_bin['safety_factor_life_per_bin'] = 0.
            elif rng > sn_1:
                _rst_dic_per_bin['log10_life'] = log10(n_0) - m_0 * (log10(rng) - log10_sn_1)
                _rst_dic_per_bin['life'] = 10 ** _rst_dic_per_bin['log10_life']
            elif rng > sn_c:
                _rst_dic_per_bin['log10_life'] = log10(n_c) - m_1 * (log10(rng) - log10(sn_c))
                _rst_dic_per_bin['life'] = 10 ** _rst_dic_per_bin['log10_life']
            elif rng > 0.:
                _rst_dic_per_bin['log10_life'] = min(log10(n_cutoff),
                        log10(n_c) + m_2 * (log10(sn_c) - log10(rng)))
                _rst_dic_per_bin['life'] = 10 ** _rst_dic_per_bin['log10_life']
            else:
                _rst_dic_per_bin['log10_life'] = log10(n_cutoff)
                _rst_dic_per_bin['life'] = n_cutoff
            if _rst_dic_per_bin['life'] > 0:
                _rst_dic_per_bin['damage_per_bin'] = cycles / _rst_dic_per_bin['life']
                if _rst_dic_per_bin['damage_per_bin'] != 0.:
                    _rst_dic_per_bin['safety_factor_life_per_bin'] = 1 / _rst_dic_per_bin['damage_per_bin']
                else:
                    _rst_dic_per_bin['safety_factor_life_per_bin'] = 1.
            _rst_dic_per_bin['safety_factor_stress'] = min(100.0, s_nb / max(1, rng))

            # store results

            res_dict['result_per_bin'][bin] = _rst_dic_per_bin
        #it+=1
    # Cumulated Damage
    
    cum_damage = 0.
    it = 0
    for bin in json_obj['stress_data'].keys():
        if it==0:
            cum_damage += res_dict['result_per_bin'][bin]['damage_per_bin']
            it+=1
    res_dict['cumulative_damage'] = cum_damage
    if cum_damage > 1e-5:
        res_dict['safety_factor_life_per_bin'] = 1. / cum_damage
        n_seqv = cycles / cum_damage
    else:
        res_dict['safety_factor_life_per_bin'] = 1e5
        n_seqv = n_cutoff

    if n_seqv <= n_0:
        s_eqv = 10 ** (log10_sn_1 + (log10(n_0) - log10(n_seqv)) / m_0)
    elif n_seqv <= n_c:
        s_eqv = 10 ** (log10(sn_c) + (log10(n_c) - log10(n_seqv)) / m_1)
    elif n_seqv < n_cutoff:
        s_eqv = 10 ** (log10(sn_c) - (log10(n_seqv) - log10(n_c)) / m_2)
    else:
        s_eqv = s_nb / 100.0
    res_dict['equivalent_stress_range'] = s_eqv
    res_dict['safety_factor_stress'] = min(100.0, s_nb / s_eqv)
    #print(json.dumps(res_dict, indent=4, sort_keys=True))
    dmg_list = []
    for key,value in res_dict["result_per_bin"].items():
        dmg_list.append(value["damage_per_bin"])
    print("dmg per bin: ", dmg_list)
    print("..........")
    print("total damage: ",sum(dmg_list))
    # insert the result to the 'Result' database
    
def apply_mean_stress_theory(mean_stress_theory,sm,rng,sn_0,r_m,r_y):
    if mean_stress_theory == 'Goodman':
        if 0. < sm:
            rng /= 1 - sm / r_m
        elif abs(sm) >= r_m:
            rng = 1.01 * sn_0
            #response[0] = 'The calculated average stress exceeds the UTS for the material.  The fatigue calculations may not be valid.  Please check the results carefully.'
    elif mean_stress_theory == 'Gerber':
        if abs(sm) < r_m:
            rng /= 1 - (sm / r_m) ** 2
        elif sm >= r_m:
            rng >= 1.01 * sn_0
            #response[0] = 'The calculated average stress exceeds the UTS for the material.  The fatigue calculations may not be valid.  Please check the results carefully.'
    elif mean_stress_theory == 'Soderberg':
        if 0. < sm < r_y:
            rng /= 1 - sm / r_y
        elif abs(sm) >= r_y:
            rng = 1.01 * sn_0
            #response[0] = 'The calculated average stress exceeds the Yield Stress for the material.  The fatigue calculations may not be valid.  Please check the results carefully.'
    else:
        pass
    return rng

start = time.time()
WeldFat(timestamp, _componentId, json_input,response)
end = time.time()
print(end - start)
