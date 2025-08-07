# app.py
import streamlit as st

# Import each simulation module's entry point
from wavelength_vs_temp_type0 import run as run_app1
from wavelength_vs_temp_type2 import run as run_app2
from pol_period_vs_temp import run as run_app3
from poling_pd_vs_temp_type0 import run as run_app5
# ... add imports for app3, app4, etc.

# ---------------------------------------------------------------------------- #
# Main SPDC Simulator Launcher
# ---------------------------------------------------------------------------- #

# Configure page once
st.set_page_config(
    page_title="SPDC Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.markdown(
    "<h1 style='text-align:center;'>🔬 SPDC Simulator for PPKTP</h1>\n"
    "<p style='text-align:center;'>Select a simulation from the dropdown below</p>",
    unsafe_allow_html=True
)

# Simulation selection dropdown
sim_choice = st.selectbox(
    "Choose a simulation:",
    [
        "— Select —",
        "Wavelength vs Temperature Type 0",#maps to app1
        "Wavelength vs Temperature Type 2",  # maps to app2
        "Poling Period vs Temperature Type 0",# maps to app5
        "Poling Period vs Temperature Type 2"
        # ... add labels for app3, app4, etc.
    ]
)

# Route to the chosen module
if sim_choice == "Wavelength vs Temperature Type 0":
    # run the UI defined in app1.py
    run_app1()

elif sim_choice == "Wavelength vs Temperature Type 2":
    # run the UI defined in app2.py
    run_app2()
elif sim_choice == "Poling Period vs Temperature Type 2":
    # run the UI defined in app3.py
    run_app3()

elif sim_choice == "Poling Period vs Temperature Type 0":
    # run the UI defined in app5.py
    run_app5()

else:
    # default message
    st.info("Please select a simulation from the dropdown.")

