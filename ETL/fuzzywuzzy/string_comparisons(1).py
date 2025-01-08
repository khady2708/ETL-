import pandas as pd

# Simple string comparison
from fuzzywuzzy import fuzz

# Compare reeding vs reading
ratio1 = fuzz.WRatio('Reeding', 'Reading')
print("ratio1:", ratio1)

# Partial string comparison
ratio2 = fuzz.WRatio('Houston Rockets', 'Rockets')
print("ratio2:", ratio2)

# Partial string comparison with different order -------------------------------------------------------------
ratio3 = fuzz.WRatio('Houston Rockets vs Los Angeles Lakers', 'Lakers vs Rockets')
print("ratio3:", ratio3)

# Import process
from fuzzywuzzy import process
# Define string and array of possible matches
string = "Houston Rockets vs Los Angeles Lakers"
choices = pd.Series(['Rockets vs Lakers', 'Lakers vs Rockets', 'Houson vs Los Angeles', 'Heat vs Bulls'])
extract = process.extract(string, choices, limit = 2)
print('extract:', extract)

# String similarity -------------------------------------------------------------------------
states = ['California', 'Cali', 'Calefornia', 'Calefornie', 'Calfornia', 'Calefernia', 'New York', 'New Yokr', 'New York City']
some_value = [1, 1, 1, 3, 0, 2, 0, 2, 4]
assert len(states) == len(some_value)
survey = pd.DataFrame({'state':states, 'some_value':some_value})
print('survey before match and replace:', survey)

# categories
categories = pd.Series({'state': ['California', 'New York']})

# For each correct category
for state in categories['state']:
    # Find potential matches in states with typoes
    matches = process.extract(state, survey['state'], limit = survey.shape[0])
    # For each potential match match
    for potential_match in matches:
        # If high similarity score
        if potential_match[1] >= 80:
            # Replace typo with correct category
            survey.loc[survey['state'] == potential_match[0], 'state'] = state

print('survey after match and replace:', survey)