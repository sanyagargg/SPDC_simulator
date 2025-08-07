import numpy as np
import matplotlib.pyplot as plt

# === Sellmeier constants from Thorlabs for Type-0 SPDC in PPKTP ===
def n_y(lambda_um):
    λ2 = lambda_um ** 2
    n2 = 2.09930 + ((0.922683 / (λ2 - 0.0467695)) - 0.0138404) * λ2
    return np.sqrt(n2)

# Wavelengths (in µm)
λ_p = 0.405
λ_s = 0.810
λ_i = 0.810

# Refractive indices
n_p = n_y(λ_p)
n_s = n_y(λ_s)
n_i = n_y(λ_i)

# Reference temperature and base poling period
T0 = 29  # Reference temperature in °C
Lambda_0 = 14.136*(λ_p / abs(n_p - n_s - n_i))  # Phase matching condition
print(Lambda_0)
# Temperature range
T = np.linspace(20, 80, 300)

# Thermal expansion of PPKTP
alpha = 6.7e-6
beta = 11e-9

# Poling period with temperature dependence
Lambda_T = Lambda_0 * (1 + alpha * (T - T0) + beta * (T - T0)**2)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(T, Lambda_T, color='darkgreen')
plt.xlabel("Temperature (°C)")
plt.ylabel("Poling Period Λ(T) (µm)")
plt.title("Poling Period vs Temperature for Type-0 SPDC in PPKTP")
plt.grid(True)
plt.ylim(3.40, 3.45)
plt.tight_layout()
plt.show()