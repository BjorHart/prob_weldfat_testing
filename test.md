
# Time Series Prediction Module

# Contents
-   [Introduction](#Introduction)
-   [Input data for Time Series Prediction module](#Input-data-for-Time-Series-Prediction-module)
	-  [Time Series Prediction data object](#Time-Series-Prediction-data-object)
	- [df object](#df-object)
	- [custom_seasonalities-object](#custom_seasonalities-object)
-   [Output data from Time Series Prediction module](#Output-data-from-Time-Series-Prediction-module)

-   [Tutorials](#Tutorials)


# Introduction
The implemented time series predictions are based on a bayesian generalized additive models (GAMs) framework. In short, this framework assumes that the observed time series  y(t)  is the sum of a trend  g(t), a seasonality  s(t)  and stochastic noise  ϵ:

![](https://latex.codecogs.com/svg.latex?\Large&space;y(t)%20=%20g(t)%20+%20s(t)%20+%20\epsilon)

The seasonality is modelled by fitting scale parameters of fourier series with chosen order and period. The trend is modeled by a linear trend with changepoints. By inferring, bayesian GAMs are able to predict over long horizons and provide uncertainty intervals for its predictions.

The Time Series Prediction module is strongly supported by the probabilistic framework PYMC3 ([https://docs.pymc.io/](https://docs.pymc.io/)).

# Input data for Time Series Prediction module

All input data for the Time Series Prediction module is sent within the `POST` payload, in the 'data' object.

### Time Series Prediction Data Object


|   |Type|Description|Required|
|---|----|-----------|--------|
|**df**|`object`|Specify history data. See __df__ object below.|Yes|
|**seasonalities**|`string`,`array`|Specify one or more of `"weekly"`,`"monthly"`,`"yearly"`. If more than one, input as list|Optional|
|**custom_seasonalities**|`object`| Specify custom seasonalities. See below for description of __custom_seasonalities__ object|Optional|
|**days_to_predict**|`number`| Specify how many days to predict|Yes|
|**CI_of_time_series**|`number`| Specify confidence interval of prediction parameters. range [0,1]|Yes|

#### df object
|   |Type|Description|Required|
|---|----|-----------|--------|
|**y**|`array`|List of history data, datatype `"float"` or `"int"` |Yes|
|**ds**|`array`| History data dates. Must be `pd.to_datetime()` castable strings(`"str"`)|Yes|

#### custom_seasonalities object

|   |Type|Description|Required|
|---|----|-----------|--------|
|**seasonality**|`number`|Specify seasonality in days |Yes|
|**fourier_order**|`number`| Specify order of fourier series to fit seasonality.|Yes|


  


# Output object from Time Series Prediction module
The result will contain the following properties:

|   |Type|Description||
|---|----|-----------|--------|
|**y_hat**|`object`|Estimated y-values. Properties:`"y_hat"`,`"y_high"` and `"y_low"` based on input confidence interval.
|**ds**|`object`|Input `df["ds"]`
|**seasonalities**|`object`|Estimated seasonality-values. Properties for each input seasonality:`"seasonality_X_hat"`,`"seasonality_X_high"` and `"seasonality_X_low"` based on input confidence interval.
|**growth**|`object`|Estimated growth-values. Properties:`"growth_hat"`,`"growth_high"` and `"growth_low"` based on input confidence interval.


# Tutorials
There is some computational time expected when using the Time Series Prediction module. Depending on your input data and applied seasonalities, it may range from 5-20 minutes. The recommended way to retrieve the results is therefore by extracting data by timestamp from the IoT Suite. 

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

######################## Specify input for Time Series Prediction ##############################
  

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
