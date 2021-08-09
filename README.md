# Boston_Evaluation

This python module estimates the price of a property in Boston.

## Docstring

```
    Estimate the price of a property in Boston.
    
    Keyword arguments:
    rm -- number of rooms in the property and it shouldn't be less than 1.
    ptratio -- number of students per teacher in the classroom for the school in the area and it shouldn't be less than 1.
    chas -- True if the property is next to the river, False otherwise. 
    large_range -- True for a 95% prediction interval, False for a 68% prediction interval. 
    
```

## How to use

```python
  import boston_valuation as bv
  
  bv.get_dollar_estimate(rm =4, ptratio = 10,  chas = True, large_range = True)

```
