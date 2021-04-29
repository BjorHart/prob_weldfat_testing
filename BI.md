# Bayesian Inference Module

## Contents
-   [Introduction](#Introduction)
-   [Input data for Bayesian Inference module](#Input-data-for-Bayesian-Inference-module)
	-  [Bayesian Inference data object](#Bayesian-Inference-data-object)
	-   [Requirements for input properties](#Requirements-for-input-properties)

-   [Output data from Bayesian Inference module](#Output-data-from-Bayesian-Inference-module)

-   [Tutorials](#Tutorials)


# Introduction

Bayesian Inference is a statistical method in which Bayes Rule is used to update a hypothesis based on observed data. With this module, a user can obtain just this, through a prior belief of a parameters distribution and observed data on that parameter.



# Input data for Bayesian Inference module

All input data for the Bayesian Inference module is send within the `POST` payload, in the 'data' object.

### Bayesian Inference Data Object

*Important*: the "data" object in the Bayesian Inference module is actually a list of objects. Each object in the list needs to have the below structure. Each object specifies one inference model. 

For each of the specified models, an array of parameters and observed values can be inferred, based on the same model. See Tutorials for further comments.

The module can be called with either one or several objects.

|   |Type|Description|Required|
|---|----|-----------|--------|
|**label**|`string`|Specify name of the inference.|Yes|
|**prior_mean_distribution**|`string`|Specify the prior mean distribution. One of `"normal"`,`"lognormal"`,`"uniform"`|Yes|
|**prior_mean_mean**|`array`| Array of means: Specify mean of the prior mean.|if prior_mean_distribution is `"normal"` or `"lognormal"`|
|**prior_mean_sd**|`array`| Array of mean sds: Specify the sd of the prior mean.|if prior_mean_distribution is `"normal"` or `"lognormal"`|
|**prior_mean_lower**|`array`| Array of lower: Specify the lower-parameter of the prior mean.|if prior_mean_distribution is `"uniform"`|
|**prior_mean_upper**|`array`| Array of upper: Specify the upper-parameter of the prior mean.|if prior_mean_distribution is `"uniform"`|
|**prior_sd**|`array`| Array of sds: Specify the prior sd of the parameter.|Yes|
|**observed**|`array of arrays`|Array of observed arrays: each element provides observed data to each of the elements of the prior variables |Yes|
|**likelihood_ditribution**|`string`|Specify likelihood distribution. One of `"normal"`,`"lognormal"`|Yes|


 


# Output object from Bayesian Inference module

|   |Type|Description|Required|
|---|----|-----------|--------|
|**posterior_summary_95**|`object`|Object with a 95% confidence summary of all inferred distributions, see posterior_summary object for more information.
|**posterior_summary_60**|`object`|Object with a 60% confidence summary of all inferred distributions, see posterior_summary object for more information.
|**predictive_distributions**|`object`|Object with posterior distribution information on the inferred distributions, se predictive_distributions object for more information.

## posterior_summary_60 (and posterior_summary_95 objects)
 
|   |Type|Description|Required|
|---|----|-----------|--------|
|**hdi_20%**|`object`|Highest density interval for all parameters, low 
|**hdi_80%**|`object`|Highest density interval for all parameters, high
|**mean**|`object`|mean of all parameters
|**sd**|`object`|sd of all parameters


## predictive_distributions object
 
|   |Type|Description|Required|
|---|----|-----------|--------|
|**posterior**|`object`|Object with posterior information, properties: `"bin_centers"`,`"bin_heights"`,`"CI_60_low"`,`"CI_60_high"`,`"CI_90_low"`,`"CI_90_high"`
|**prior**|`object`|Object with prior information, properties: `"bin_centers"`,`"bin_heights"`,`"CI_60_low"`,`"CI_60_high"`,`"CI_90_low"`,`"CI_90_high"`


# Tutorials
There is some computational time expected when using the Time Series Prediction module. Depending on your input data and applied seasonalities, it may range from 5-20 minutes. The recommended way to retrieve the results is therefore to extract result by timestamp from the IoT Suite. 

The tutorial below show-cases an end to end example:

```python
import requests
import json
import time

###################### Connection details #########################
base_url = "https://edrmedesoapiservice.azurewebsites.net/"
username = %YOUR_USERNAME%
password = %YOUR_PASSWORD%

# First Get token. You need to provide username and password
login = {'username': username, 'password': password}
req_type = {"Content-Type": "application/json"}
url = base_url + "getToken"
response = requests.request("GET", url, headers=req_type, data=json.dumps(login))

# Save the token
token = response.text

######################## Specify input for Bayesian Inference ##############################
  

df = %YOUR DATA: A DICTIONARY WITH KEYS = ["ds","y"]%
  

run_specifications = {

	"df": df,
	"seasonalities": ["weekly", "monthly"],
	"custom_seasonalities": [{"seasonality":10,"fourier_order":4},{"seasonality":12,"fourier_order":2}],
	"days_to_predict":60,
	"CI_of_time_series":0.95,
}

######################## Send specifications to Time Series Prediction ##############################


url = "{}inputData?token={}".format(base_url, token)
payload = {
	"componentId": %YOUR_COMPONENT_ID%,
	"destinationModule": "TimeSeriesPrediction",
	"data": run_specifications
}

response = requests.request("POST", url, headers=req_type, data=json.dumps(payload))

# get timestamp, this is the timestamp used for getting results
timestamp = json.loads(response_post.text)["timestamp"] 




##################### Getting the prediction results ###############

payload["timestamp"] = timestamp
url = "{}GetResultByTimeStamp?token={}".format(base_url, token)

time.sleep(600) # Wait for prediction to finish. 10 minutes may not be sufficient

response = requests.request('GET', url, headers=req_type, data=json.dumps(payload))

results = json.loads(response.text)


```
