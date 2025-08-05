import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    # === Sellmeier Equation for PPKTP (Type-0 SPDC) ===
    def n_y(lambda_um):
        λ2 = lambda_um ** 2
        n2 = 2.09930 + ((0.922683 / (λ2 - 0.0467695)) - 0.0138404) * λ2
        return np.sqrt(n2)

    # Constants
    λ_p = 0.405
    λ_s = 0.810
    λ_i = 0.810
    T0 = 29  # reference temperature

    # Refractive indices
    n_p = n_y(λ_p)
    n_s = n_y(λ_s)
    n_i = n_y(λ_i)

    # Initial poling period for perfect phase-matching
    Lambda_0 = 14.136 * (λ_p / abs(n_p - n_s - n_i))

    # Thermal expansion coefficients
    alpha = 6.7e-6
    beta = 11e-9

    # === SIDEBAR CONTROLS ===
    st.sidebar.header("🔧 OVERALL GRAPH CONTROLS")

    # Temperature limits
    st.sidebar.markdown("---")
    st.sidebar.header("🌡️ Temperature Range Settings")
    min_temp = st.sidebar.number_input("Minimum slider limit (°C):", value=0, min_value=-100, max_value=200)
    max_temp = st.sidebar.number_input("Maximum slider limit (°C):", value=120, min_value=-100, max_value=200)

    if min_temp >= max_temp:
        st.sidebar.error("Minimum limit must be less than maximum limit.")
        st.stop()

    # Slider for temperature range
    T_min, T_max = st.sidebar.slider("Select Temperature Range (°C):", min_temp, max_temp, (20, 80))

    # Precision dropdown
    st.sidebar.markdown("---")
    st.sidebar.header("📏 Display Precision")
    decimal_places = st.sidebar.selectbox("Decimal Places for Λ(T):", [2, 3, 4, 5, 6], index=3)

    # Lookup Temperature
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Lookup")
    T_lookup = st.sidebar.number_input("Lookup Temperature (°C):", min_value=min_temp * 1.0, max_value=max_temp * 1.0, value=29.0, step=0.1)

    # === CALCULATION ===
    steps = 300
    T = np.linspace(T_min, T_max, steps)
    Lambda_T = Lambda_0 * (1 + alpha * (T - T0) + beta * (T - T0)**2)
    Lambda_T = np.round(Lambda_T, decimals=decimal_places)

    Lambda_lookup = Lambda_0 * (1 + alpha * (T_lookup - T0) + beta * (T_lookup - T0)**2)
    Lambda_lookup = round(Lambda_lookup, decimal_places)

    # Y-axis range (AFTER Lambda_T calculation)
    st.sidebar.markdown("---")
    st.sidebar.header("📐 Y-axis Range for Poling Period")
    ymin_user = st.sidebar.number_input("Y-axis Min (Λ)", value=float(np.min(Lambda_T) - 0.001), step=0.0001, format="%.4f")
    ymax_user = st.sidebar.number_input("Y-axis Max (Λ)", value=float(np.max(Lambda_T) + 0.001), step=0.0001, format="%.4f")

    # === MAIN DISPLAY ===
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 36px;'>
            📈 <span style="color: #4dd0e1;">Poling Period</span> vs <span style="color: #ba68c8;">Temperature</span><br>
            <span style="font-size: 22px; color: gray;">(Type-0 SPDC in PPKTP)</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='text-align: center; background-color: #e0f2ff; padding: 10px; border-radius: 10px;
                    font-size: 22px; font-weight: bold; border: 1px solid #90caf9; color: #000000;'>
            Λ({T_lookup:.1f} °C) = {Lambda_lookup:.{decimal_places}f} µm
        </div>
        """, unsafe_allow_html=True
    )

    # === PLOT ===
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        T, Lambda_T,
        color="#1e88e5",  # Blue that works in both modes
        linewidth=2,
        linestyle='-',
        marker='',
        label=f"Λ(T), rounded to {decimal_places} decimals"
    )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Poling Period Λ(T) (µm)")
    ax.set_title("Poling Period vs Temperature")
    ax.grid(True)
    ax.set_ylim(ymin_user, ymax_user)
    ax.legend()

    st.pyplot(fig)
