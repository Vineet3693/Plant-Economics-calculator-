
"""Constants for Plant Economics Calculator"""

# Depreciation methods
DEPRECIATION_METHODS = [
    "Straight Line",
    "Declining Balance", 
    "Sum of Years Digits",
    "Sinking Fund"
]

# Lang factors by industry
LANG_FACTORS = {
    "Solid Processing": 3.1,
    "Solid-Fluid Processing": 4.3,
    "Fluid Processing": 4.8,
    "Chemical Processing": 4.3,
    "Petrochemical": 5.5
}

# Scaling exponents by equipment type
SCALING_EXPONENTS = {
    "General Equipment": 0.6,
    "Compressors": 0.8,
    "Heat Exchangers": 0.7,
    "Pumps": 0.5,
    "Reactors": 0.6,
    "Distillation Columns": 0.65
}
