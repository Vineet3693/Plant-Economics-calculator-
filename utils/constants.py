"""Application constants and reference data"""
# Lang Factors for different industries
LANG_FACTORS = {
    'Chemical Processing': 4.5,
    'Petrochemical': 4.2,
    'Pharmaceutical': 5.5,
    'Food Processing': 3.8,
    'Oil Refining': 4.0,
    'General Chemical': 4.3
}

# Scaling Exponents for equipment sizing
SCALING_EXPONENTS = {
    'Heat Exchangers': 0.65,
    'Pumps': 0.35,
    'Compressors': 0.75,
    'Reactors': 0.65,
    'Distillation Columns': 0.70,
    'Default': 0.6
}

# Depreciation Methods
DEPRECIATION_METHODS = [
    'Straight Line',
    'Declining Balance',
    'Sum of Years Digits',
    'Sinking Fund'
]

# Currency symbols
CURRENCY_SYMBOL = "$"

# Percentage format
PERCENTAGE_FORMAT = "{:.2f}%"

# Money format
MONEY_FORMAT = "${:,.2f}"
