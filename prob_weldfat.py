import numpy as np
import theano
import theano.tensor as tt
import pymc3 as pm
import matplotlib.pyplot as plt
from theano.ifelse import ifelse
import json
from input import *
from WeldFat_Pref import *
import rainflow
import time
from math import *

theano.config.optimizer='fast_compile'
theano.config.exception_verbosity='high'
theano.config.compute_test_value = 'warn'

def unpack_weldfat(json_input):
    """
        Unpacks input json
        to theano readable parameters
    """
    #unpacking function:
    stress_unit_dict = {'mpa': 1.0, 'psi': 145.038, 'ksi': 0.145038} #Mpa to user unit

    json_obj = {}
    json_obj = json.loads(json_input)
    kwargs = {}
    
    if 'class' not in json_obj['fatigue_class']:
        fat_class = 'User defined'
        #kwargs["fat_class"] = 'User defined'
        kwargs["fat"] = json_obj['fatigue_class']['fat'] 
        kwargs["n_fat"] = json_obj['fatigue_class']['n_fat']
        kwargs["n_c"] = json_obj['fatigue_class']['n_c']
        kwargs["m_1"] = json_obj['fatigue_class']['m_1']
        kwargs["m_2"] = json_obj['fatigue_class']['m_2']
    else:
        fat_class = json_obj['fatigue_class']['class']
        if fat_class in fatClassDict:
            kwargs["fat"] = fatClassDict[fat_class]['FAT'][0] * stress_unit_dict[fatClassDict[fat_class]['FAT'][1].lower()]#SN curve in MPa change to user unit
            kwargs["n_fat"] = fatClassDict[fat_class]['Nfat']
            kwargs["n_c"] = fatClassDict[fat_class]['Nc']
            kwargs["m_1"] = fatClassDict[fat_class]['m1']
            kwargs["m_2"] = fatClassDict[fat_class]['m2']
        else:
            response[0] = fat_class + ' not found in fatClassDict - not catch json schema validator'

    if 'fat_fact' not in json_obj['fatigue_class']:
        kwargs["fat_fact"] = 1.
    else:
        kwargs["fat_fact"] = json_obj['fatigue_class']['fat_fact']

    if 'N0' in fatClassDict[fat_class]:
        kwargs["n_0"] = fatClassDict[fat_class]['N0']
    else:
        kwargs["n_0"] = 1

    if 'm0' in fatClassDict[fat_class]:
        kwargs["m_0"] = fatClassDict[fat_class]['m0']
    else:
        kwargs["m_0"] = 1

    if 'Ncutoff' in fatClassDict[fat_class]:
        kwargs["n_cutoff"] = fatClassDict[fat_class]['Ncutoff']
    else:
        kwargs["n_cutoff"] = 1

    if 'mean_stress_theory' in json_obj:
        kwargs["mean_stress_theory"] = json_obj['mean_stress_theory']
        mean_stress_theory = kwargs['mean_stress_theory']['theory']
        if mean_stress_theory in ['Goodman', 'Gerber']:
            kwargs["r_m"] = kwargs['mean_stress_theory']['ultimate_limit']
            kwargs["r_y"] = 0.9 * kwargs["r_m"]
            if mean_stress_theory=="Goodman":
                m_s_th = 1
            else: #Gerber
                m_s_th = 2
        elif mean_stress_theory == 'Soderberg':
            kwargs["r_m"] = 0.
            kwargs["r_y"] = kwargs['mean_stress_theory']['yield_limit']
            m_s_th = 3
    else:
        m_s_th = 0
    kwargs["m_s_th"] = m_s_th
    del kwargs["mean_stress_theory"]


    if 'stress_data' not in json_obj.keys() and 'serie_data' in json_obj.keys():
        series = json_obj['serie_data']['series']
        if series ==[]:
            response[0] = 'serie '+str(series)+' not valid'
            return
        if 'nbins' in json_obj['serie_data'].keys():
            kwargs["max_range"] = max(series) - min(series)
            if 'maxrange' in json_obj['serie_data']:
                kwargs["my_max_range"] = json_obj['serie_data']['maxrange']
                kwargs["max_range"] = kwargs["my_max_range"]
                if kwargs["max_range"] < kwargs["my_max_range"]:  
                    pass
                else:
                    response[0] = 'Warning: serie max range larger than given max range'
                    
            kwargs["nbins"] = json_obj['serie_data']['nbins']
            kwargs["binsize"] = kwargs["max_range"] / kwargs["nbins"]
            
            kwargs["counts_ix"] = defaultdict(int)
            for i in range(kwargs["nbins"]):
                 kwargs["counts_ix"][i] = 0

            # Apply mean stress theory before assigning to bin

            for (rng, mean, count, i_start, i_end) in rainflow.extract_cycles(series):
            
                if 'mean_stress_theory' in json_obj:
                    kwargs["sn_0_user_unit"]= kwargs["sn_0"]
                    kwargs["rng"] = apply_mean_stress_theory(kwargs["mean_stress_theory"],mean,rng,kwargs["sn_0_user_unit"],kwargs["r_m"],kwargs["r_y"])
                kwargs["bin_index"] = int(abs(rng) / kwargs["binsize"])

                # handle possibility of range equaliing max range

                if kwargs["bin_index"] == kwargs["nbins"]:
                    kwargs["bin_index"] = kwargs["nbins"] - 1
                kwargs["counts_ix"][kwargs["bin_index"]] += count

            # save count data to dictionary where key is the range

            kwargs["counts"] = dict(((k + 1) * kwargs["binsize"], v) for (k, v) in kwargs["counts_ix"].items())
            kwargs["cycles_list"] = sorted(kwargs["counts"].items())

            kwargs["stress_data"] = {}
            
            for i in range(len(kwargs["cycles_list"])):
                kwargs["stress_data"][i] = {'rng': kwargs["cycles_list"][i][0], 'cycles': kwargs["cycles_list"][i][1], 'sm': 0.}
            if 'mean_stress_theory' in json_obj:
                del json_obj['mean_stress_theory']
        elif 'maxrange' in json_obj['serie_data'].keys() and not 'nbins' in json_obj['serie_data'].keys():
            response[0] = '"maxrange" and no "nbins" not currently handle - not catch json schema validator'
        else:
            kwargs['cycles'] = []
            kwargs['rng'] = []
            kwargs['sm'] = []
            
            for (i, (rng, mean, count, i_start, i_end)) in enumerate(rainflow.extract_cycles(series)):
                kwargs["cycles"].append(count)
                kwargs["rng"].append(rng)
                kwargs["sm"].append(mean)
    #print(json.dumps(kwargs, indent=4, sort_keys=True))
    return kwargs


def apply_mean_stress_theory(m_s_th,sm,rng,sn_0,r_m,r_y):
    rng = ifelse(tt.eq(1,m_s_th),
            ifelse(tt.lt(0,sm),rng/(1-(sm/r_m)),
                ifelse(tt.le(r_m,tt.abs_(sm)),1.01 * sn_0,rng)),
        ifelse(tt.eq(2,m_s_th),
            ifelse(tt.lt(tt.abs_(sm),r_m),rng/(1-(sm/r_m)**2),
                ifelse(tt.le(r_m,sm),1.01*sn_0,rng)),
        ifelse(tt.eq(3,m_s_th),
            ifelse(tt.lt(0,sm) & tt.lt(sm,r_y),rng/1-(sm/r_y),
            ifelse(tt.le(r_y,tt.abs_(sm)),1.01*sn_0,rng)),rng)))
    return rng

def fn(cycles,rng,sm,cum_dmg,sn_0,sn_c,sn_cutoff,fat, n_fat, n_c, m_1, m_2,fat_fact, n_0, m_0, n_cutoff,r_y, r_m,m_s_th): # y is previous result
    """
        input function to the loop over all bins
    """
    cum_damage = np.float64(0)
    log10_sn_1 = (tt.log10(fat * fat_fact) + (tt.log10(n_fat) - tt.log10(n_0)) / m_1).astype("float64")
    sn_1 = 10 ** log10_sn_1
    sn_0 = (10 ** (log10_sn_1 + tt.log10(n_0) / m_0)).astype("float64")
    sn_c = (10 ** (tt.log10(fat * fat_fact) - (tt.log10(n_c) - tt.log10(n_fat)) / m_1)).astype("float64")
    sn_cutoff = (10 ** (tt.log10(sn_c) - (tt.log10(n_cutoff)-tt.log10(n_c))/m_2)).astype("float64")
    life = 0
    log10_life = 0
    dmg_per_bin = 0
    s_factor_life_per_bin = 0 
    s_factor_stress_per_bin = 0
    s_nb = ifelse(tt.neq(cycles,0),
        ifelse(tt.le(cycles,n_0),(10 ** (log10_sn_1 + (tt.log10(n_0) - tt.log10(cycles))/ m_0)),
            ifelse(tt.le(cycles,n_c),(10 ** (tt.log10(sn_c) + (tt.log10(n_c) - tt.log10(cycles)) / m_1)),10 ** (tt.log10(sn_c) - (tt.log10(cycles) - tt.log10(n_c)) / m_2))),0*cycles)
            
    rng = ifelse(tt.neq(m_s_th,0) & tt.neq(sm,0),ifelse(tt.neq(sm,0),apply_mean_stress_theory(m_s_th,sm,rng,sn_0,r_m,r_y),rng),rng) # double check if 0 = False
    log10_life,life,dmg_per_bin,s_factor_life_per_bin = ifelse(tt.lt(sn_0,rng),[np.float64(-1),np.float64(0),np.float64(100),np.float64(0)],
        ifelse(tt.lt(sn_1,rng),[(tt.log10(n_0) - m_0 * (tt.log10(rng) - log10_sn_1)),(10 **(tt.log10(n_0) - m_0 * (tt.log10(rng) - log10_sn_1))),np.float64(0),np.float64(0)], 
        ifelse(tt.lt(sn_c,rng),[(tt.log10(n_c) - m_1 * (tt.log10(rng) - tt.log10(sn_c))),(10 **(tt.log10(n_c) - m_1 * (tt.log10(rng) - tt.log10(sn_c)))),np.float64(0),np.float64(0)],
        ifelse(tt.lt(0,rng),[(tt.min([tt.log10(n_cutoff),
                tt.log10(n_c) + m_2 * (tt.log10(sn_c) - tt.log10(rng))])),(10 ** tt.min([tt.log10(n_cutoff),
                tt.log10(n_c) + m_2 * (tt.log10(sn_c) - tt.log10(rng))])).astype("float64"),np.float64(0),np.float64(0)],
                [tt.log10(n_cutoff).astype("float64"),n_cutoff.astype("float64"),np.float64(0),np.float64(0)]

        )
        )
        ))

    dmg_per_bin = ifelse(tt.lt(0,life),cycles / life, 0*life)#_rst_dic_per_bin['life'] > 0:
    s_factor_life_per_bin = ifelse(tt.neq(dmg_per_bin, 0.), 1 / dmg_per_bin, np.float64(1))
    s_factor_stress_per_bin = tt.min([100.0, s_nb / tt.max([1, rng])])


    return  dmg_per_bin,sn_0,sn_c,sn_cutoff


def scan(cycles,rng,sm,fat: int=1, n_fat: int = 2000000, n_c: int=10000000, m_1:int=3, m_2:int=22,fat_fact: int=1, n_0: int=314018, m_0: int=5, n_cutoff: int=10000000000,r_y:int=0, r_m:int=0, m_s_th:int=0):
        """
            scan is a theano equivalent to a loop
        """
        
        #s_x = T.ivector("name")
        dmg_per_bin = tt.as_tensor_variable(np.float64())
        sn_0 = tt.as_tensor_variable(np.float64())
        sn_c = tt.as_tensor_variable(np.float64())
        sn_cutoff = tt.as_tensor_variable(np.float64())
        #n = T.iscalar()
        s_y, update_sum = theano.scan(
            fn=fn,
            sequences = [cycles,rng,sm],
            outputs_info = [dmg_per_bin,sn_0,sn_c,sn_cutoff],
            #n_steps=len(x),
            non_sequences=[fat,n_fat,n_c,m_1,m_2,fat_fact,n_0,m_0,n_cutoff,r_y,r_m,m_s_th] # essentially the parameters one can apply dists to
        )
        #res_ = s_y[-1]
        return s_y

def calculate_weldfat(**kwargs):
    """ takes the unpacked input-json as keyword arguments and performs weldfat
        calulations.
    """
    cycles = tt.as_tensor_variable(kwargs["cycles"])
    rng = tt.as_tensor_variable(kwargs["rng"])
    sm = tt.as_tensor_variable(kwargs["sm"])
    del kwargs["cycles"], kwargs["rng"], kwargs["sm"]
    
    with pm.Model() as model:
        dists = {"normal":pm.Normal,"halfnormal":pm.HalfNormal, "lognormal": pm.Lognormal, "uniform":pm.Uniform}
        distributed=False
        for key,value in kwargs.items():
            if type(value)==list and (value[0] in ["normal","halfnormal","lognormal","uniform"]):
                distributed=True # triggers sampling process
                kwargs[key] = dists[value[0]](str(key)+ "dist",mu=value[1],sd=value[2])
        else:
            hei=1
           
        dmg_per_bin,sn_0,sn_c,sn_cutoff = scan(cycles,rng,sm,**kwargs)
        sn_0 = pm.Deterministic("sn_0", sn_0)
        sn_c = pm.Deterministic("sn_c", sn_c)
        sn_cutoff = pm.Deterministic("sn_cutoff", sn_cutoff)
        dmg_per_bin = pm.Deterministic('dmg_per_bin',dmg_per_bin)
        acc_dmg =pm.Deterministic('acc_dmg',tt.sum(dmg_per_bin))
        trace = []
        if distributed:
            trace = pm.sample(target_accept=0.9)
            dmg_per_bin = trace["dmg_per_bin"]
            acc_dmg = trace["acc_dmg"]
        else:
            #theano.
            dmg_per_bin = dmg_per_bin.eval()
            acc_dmg = acc_dmg.eval()
            print(dmg_per_bin,"\n", acc_dmg)
        
    return trace, dmg_per_bin, acc_dmg 

def plot_trace(trace,kwargs):
    if len(trace):
        pm.traceplot(trace)
        plt.savefig("accumulated_dmg_in_batch")
        plt.close()
        acc_dmg_trace = trace["acc_dmg"]
        
        heights,edges = plt.hist(acc_dmg_trace,bins=100)[:2]
        binWidX = edges[1] - edges[0]
        centers = edges[:-1] + binWidX/2
        mean = acc_dmg_trace.mean()
        std = acc_dmg_trace.std()

        print("mean: ",mean, "std: ",std)

        x_coords =[mean,mean-std,mean+std]
        for x in x_coords:
            plt.axvline(x=x, color="red")
            plt.text(x,5,x,rotation=90)
        
        plt.savefig("acc_dmg")
        plt.close()

##################
        #save all sn-curves as plot
        sn_0 = trace["sn_0"].T[0]
        sn_c = trace["sn_c"].T[0]
        sn_cutoff = trace["sn_cutoff"].T[0]
        sn_0 = [log10(i) for i in sn_0]
        sn_c = [log10(i) for i in sn_c]
        sn_cutoff = [log10(i) for i in sn_cutoff]
        n_cutoff = log10(1e10)
        n_1 = log10(1)
        if "n_c" in trace.varnames:
            n_c = trace["n_c"].T[0]
            n_c = [log10(i) for i in n_c]
            for i in sn_0:
                plt.plot([n_1,n_c[i],n_cutoff],[sn_0,sn_c,sn_cutoff])
        else: 
            n_c = log10(kwargs["n_c"])
            plt.plot([n_1,n_c,n_cutoff],[sn_0,sn_c,sn_cutoff], color='C3',alpha=0.005)
        
        plt.savefig("sn_curves")
##################

    else:
        print("no trace to plot")
        


start = time.time()
# do calculation
kwargs = unpack_weldfat(input())
trace,dmg_per_bin,acc_dmg = calculate_weldfat(**kwargs)
##################
end = time.time()

print(end - start)

plot_trace(trace,kwargs)