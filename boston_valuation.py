from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

# Gather Data 
boston_dataset = load_boston()

# Create a Pandas dataframe 
data = pd.DataFrame(data=boston_dataset.data, columns=boston_dataset.feature_names)

# Drop two features from data set
features = data.drop(['INDUS', 'AGE'], axis=1)

# Convert price to log price and convert to dataframe
log_price = np.log(boston_dataset.target)
target = pd.DataFrame(data=log_price, columns=['PRICE'])

CRIME_IDX = 0
ZN_IDX = 1
CHAS_IDX = 2
RM_IDX = 4
PTRATIO_IDX = 8

# Get current dollar price value
current_price_dollar_value = 685.5 # zillow price
scale_factor = current_price_dollar_value / np.median(boston_dataset.target)

# Average values for all features
property_stats = features.mean().values.reshape(1, 11)

# Regression and fitted values calculation
regression = LinearRegression().fit(features, target)
fitted_vals = regression.predict(features)

# MSE and RMSE calculation
MSE = mean_squared_error(target, fitted_vals)
RMSE = np.sqrt(MSE)

def get_log_estimate(no_rooms,
                    student_per_classroom,
                    next_to_river = False,
                    high_confidence = True):
    
    # Configure Property
    property_stats[0][RM_IDX] = no_rooms
    property_stats[0][PTRATIO_IDX] = student_per_classroom
    
    if next_to_river:
           property_stats[0][CHAS_IDX] = 1
    else:
        property_stats[0][CHAS_IDX] = 0
        
       
    # Make Prediction
    log_estimate = regression.predict(property_stats)[0][0]
    
    # Calculate Range
    if high_confidence:
        upper_bound = log_estimate + 2 * RMSE
        lower_bound = log_estimate - 2 * RMSE
        interval = 95
    else:
        upper_bound = log_estimate + RMSE
        lower_bound = log_estimate - RMSE
        interval = 68

    return log_estimate, upper_bound, lower_bound, interval 


def get_dollar_estimate(rm, ptratio, chas = False, large_range = True):
    
    """Estimate the price of a property in Boston.
    
    Keyword arguments:
    rm -- number of rooms in the property and it shouldn't be less than 1.
    ptratio -- number of students per teacher in the classroom for the school in the area and it shouldn't be less than 1.
    chas -- True if the property is next to the river, False otherwise. 
    large_range -- True for a 95% prediction interval, False for a 68% prediction interval. 
    
    
    """
    
    if rm < 1 or ptratio < 1:
        print('Kindly input a realistic value!')
        return
    
    log_estimate, upper, lower, conf = get_log_estimate(no_rooms=rm,
                                                       student_per_classroom=ptratio,
                                                       next_to_river=chas,
                                                       high_confidence=large_range)
    
    # Convert to today dollar price
    dollar_price = np.around((np.e**log_estimate * 1000 * scale_factor), -3)
    dollar_upper_bound = np.around((np.e**upper * 1000 * scale_factor), -3)
    dollar_lower_bound = np.around((np.e**lower * 1000 * scale_factor), -3)
    
    print(f'The estimated property value is ${dollar_price}.')
    print(f'At {conf}% confidence the valuation range is')
    print(f'${dollar_lower_bound} at the lower bound and ${dollar_upper_bound} at the upper bound')


