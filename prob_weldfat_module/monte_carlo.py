import jsonschema
from json_schema import *
from input_json import *
from weldfat import *
import time

jsonschema.validate(json.loads(input_json),json.loads(weldfat_schema))
print("hei")

timestamp=1
_componentId="aaa"
response=[""]


def monte_carlo(timestamp,_componentId,response,samples:int=1000,**kwargs):
    dists = {"normal":norm,"halfnormal":halfnorm, "lognormal": lognorm, "uniform":uniform}
    distributed=False

    for key,value in kwargs["fatigue_class"].items():
        if type(value)==dict:
            distributed=True # triggers sampling process
            kwargs["fatigue_class"][key] = list(dists[value["d"]](loc=value["m"],scale=value["sd"]).rvs(samples))
    if "mean_stress_theory" in kwargs.keys():
        if "yield_limit" in kwargs["mean_stress_theory"].keys() and  type(kwargs["mean_stress_theory"]["yield_limit"])==dict:
            kwargs["mean_stress_theory"]["yield_limit"] = list(dists[kwargs["mean_stress_theory"]["yield_limit"]["d"]](loc=kwargs["mean_stress_theory"]["yield_limit"]["m"],scale=kwargs["mean_stress_theory"]["yield_limit"]["sd"]).rvs(samples))
            distributed=True # triggers sampling process
        elif type(kwargs["mean_stress_theory"]["ultimate_limit"])==dict:
            kwargs["mean_stress_theory"]["ultimate_limit"] = list(dists[kwargs["mean_stress_theory"]["ultimate_limit"]["d"]](loc=kwargs["mean_stress_theory"]["ultimate_limit"]["m"],scale=kwargs["mean_stress_theory"]["ultimate_limit"]["sd"]).rvs(samples))
       
    if distributed:
        kwargs_sample = copy.deepcopy(kwargs) # kwargs for sampling process
        results = {}
        results["dmg_list"] = []
        results["sn_0"] = []
        results["sn_c"] = []
        results["sn_cutoff"] = []
        results["n_c"] = []
        for i in range(samples):
            for key,value in kwargs["fatigue_class"].items():
                if type(value)==list:
                    kwargs_sample["fatigue_class"][key] = value[i]
            if "mean_stress_theory" in kwargs.keys():
                if "yield_limit" in kwargs["mean_stress_theory"] and type(kwargs["mean_stress_theory"]["yield_limit"])==list:
                        kwargs_sample["mean_stress_theory"]["yield_limit"] = kwargs["mean_stress_theory"]["yield_limit"][i]
                if "ultimate_limit" in kwargs["mean_stress_theory"] and type(kwargs["mean_stress_theory"]["ultimate_limit"])==list:
                        kwargs_sample["mean_stress_theory"]["ultimate_limit"] = kwargs["mean_stress_theory"]["ultimate_limit"][i]
                
                #if key=="mean_stress_theory" and kwargs_sample["fatigue_class"][key]:
                    
            dmg_list,sn_0,sn_c,sn_cutoff,n_c = WeldFat(timestamp, _componentId, json.dumps(kwargs_sample),response)
            results["dmg_list"].append(dmg_list)
            results["sn_0"].append(sn_0)
            results["sn_c"].append(sn_c)
            results["sn_cutoff"].append(sn_cutoff)
            results["n_c"].append(n_c)

    else:
        results = WeldFat(timestamp, _componentId, json.dumps(kwargs),response)

    return results    


def plot_trace(results):
    dmg_list = np.array(results["dmg_list"])
    acc_dmg_list = np.sum(dmg_list,axis=1)
    sn_0 = np.array(results["sn_0"])
    sn_c = np.array(results["sn_c"])
    sn_cutoff = np.array(results["sn_cutoff"])
    sn_0 = [log10(i) for i in sn_0]
    sn_c = [log10(i) for i in sn_c]
    sn_cutoff = [log10(i) for i in sn_cutoff]

    n_cutoff = log10(1e10)
    n_c = np.array(results["n_c"])
    n_c = [log10(i) for i in n_c]
    n_1 = log10(1)
    #n_1 = results["n_1"]
    

    plt.hist(acc_dmg_list,bins=100)[:2]
    mean = acc_dmg_list.mean()
    std = acc_dmg_list.std()

    print("mean: ",mean, "std: ",std) 
    
    x_coords =[mean,mean-std,mean+std]
    for x in x_coords:
        plt.axvline(x=x, color="red")
        plt.text(x,5,x,rotation=90)
    
    plt.savefig("hist_orig_weldfat")
    plt.close()

    for i in range(len(sn_0)):
        plt.plot([n_1,n_c[i],n_cutoff],[sn_0[i],sn_c[i],sn_cutoff[i]],color='C3',alpha=0.005)
    #plt.xlim([6,7])
    plt.savefig("sn_curves_orig_weldfat")
    plt.close()  

    plt.plot(n_c)
    plt.savefig("sn_c")
    plt.close



start = time.time()
#WeldFat(timestamp, _componentId, json_input,response)
results = monte_carlo(timestamp,_componentId,response,**json.loads(input_json))

end = time.time()
print(end - start)
if len(results["dmg_list"]):
    plot_trace(results)
