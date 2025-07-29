import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# Sellmeier + thermo-optic equations
#Thorlabs
def sellmeier(w, pol):
    if pol == 'z':
        return np.sqrt(np.abs(
          2.12725 + (1.18431 / (w**2 - 0.0514852 ) + 0.6603 / (w**2 - 100.00507 ) - 9.68956e-3) * (w**2)
        ))
    else:
        return np.sqrt(np.abs(
            2.09930 + (0.922683 / (w**2 - 0.0467695 ) - 0.0138404) * (w**2)
        ))
def temperature_dependence(w, pol):
    if pol == "z":
        return (1e-6 * (4.1010 * w**-3 - 8.9603 * w**-2 + 9.9228 * w**-1 + 9.9587) +
                1e-8 * (3.1481 * w**-3 - 9.8136 * w**-2 + 10.459 * w**-1 - 1.1882))
    else:
        return (1e-6 * (2.6486 * w**-3 - 6.0629 * w**-2 + 6.3061 * w**-1 + 6.2897) +
                1e-8 * (1.3470 * w**-3 - 3.5770 * w**-2 + 2.2244 * w**-1 - 0.14445))
def n(w, T, pol):
    return sellmeier(w, pol) + temperature_dependence(w, pol) * (T - 25)
# poling period computation (Type-0)
def poling_period(w1, w2, w3, T):
    return 1 / (n(w3, T, "z") / w3 - n(w2, T, "z") / w2 - n(w1, T, "z") / w1)

# Solve for w1 given fixed QPM period and w3
def solve_w1_for_period(target_period, w3, T):
    def equation(w1):
        w2 = 1 / (1 / w3 - 1 / w1)
        return poling_period(w1, w2, w3, T) - target_period

    # Use Newton-Raphson method
    w1_guess = 1 / (1 / w3 - 1 / 0.9)  # μm
    return newton(equation, w1_guess)

# Temperature range
temps = np.arange(25, 76, 1)  # °C
w3 = 0.405  # μm (pump)
T0 = 25  # reference temperature
w1_ref = 1 / (1 / w3 - 1 / 0.81)  # non-degenerate example
w2_ref = 1 / (1 / w3 - 1 / w1_ref)
Λ_fixed = poling_period(w1_ref, w2_ref, w3, T0)

idler_list = []
signal_list = []

for T in temps:
    try:
        w1 = solve_w1_for_period(Λ_fixed, w3, T)
        w2 = 1 / (1 / w3 - 1 / w1)
        idler_list.append(w1 * 1000)  # nm
        signal_list.append(w2 * 1000)
    except RuntimeError:
        idler_list.append(np.nan)
        signal_list.append(np.nan)

# Plot
plt.figure(figsize=(8,5))
plt.plot(temps, idler_list, label="Idler [nm]", marker='o')
plt.plot(temps, signal_list, label="Signal [nm]", marker='x')
plt.xlabel("Temperature [°C]")
plt.ylabel("Wavelength [nm]")
plt.title("Wavelength vs Temperature (PPKTP, Type-0 SPDC)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
