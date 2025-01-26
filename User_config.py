# config.py

# Authors
# Shunmuga Priya Subbiah,WAREM
# Hedieh Beigi Pouya,WAREM
# Mohammad Sharif Khaleqi,WAREM
try:
    import os
    import logging
except ImportError:
    print("ERROR: Cannot import basic Python libraries.")
try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("ERROR: Cannot import SciPy libraries.")

try:
    import plotly.graph_objects as go
    import plotly.offline as pyo
except ImportError:
    print("ERROR: Cannot import plotly.graph_objects,plotly.offline packages.")

# File paths
CSV_FILE_NAME = "data/CAMELS_GB_hydromet_timeseries_12007.csv"
OUTPUT_FILE = "runoff_with_discharge_output"

# Snow parameters
TT = 0  # Threshold temperature for snow accumulation
Cmelt = 15  # Melting coefficient
SWE_INITIAL = 0  # Initial snow water equivalent

# Evapotranspiration parameters
PWP = 100  # Permanent Wilting Point (mm)
INITIAL_SOIL_MOISTURE = 10  # Initial soil moisture (mm)
FIELD_CAPACITY = 300  # Field Capacity (mm)

# Soil moisture parameters
BETA = 2
K = 0.5
TIME_STEP = 1  # Example time step (daily)
CATCHMENT_AREA= 289*1000000
mm_to_m = 1 / 1000  # Conversion factor from mm to m
day_to_s = 1 / (24 * 3600)  # Conversion factor from day to seconds
ENABLE_PLOTTING = True

