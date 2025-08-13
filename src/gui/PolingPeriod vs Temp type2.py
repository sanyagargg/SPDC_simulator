import numpy as np
import matplotlib.pyplot as plt

# --- Wavelengths in microns ---
lambda_p = 0.4062  # pump (extraordinary/z-axis)
lambda_s = 0.8124  # signal (ordinary/y-axis)
lambda_i = 0.8124  # idler (extraordinary/z-axis)

# --- Temperature range ---
temperatures = np.linspace(20, 120, 200)

# --- Sellmeier Coefficients from thesis ---

# Ordinary (y-axis)
A_y = 2.19229
B_y = 0.83547
C_y = 0.04970
D_y = 0.01621

# Extraordinary (z-axis)
A_z = 2.12725
B_z = 1.18431
C_z = 0.0514852
D_z = 0.6603
E_z = 100.00507
F_z = 9.68956e-3

# --- Thermal expansion coefficients ---
A_exp = 6.7e-6    # linear
B_exp = 11e-9     # quadratic
F_temp = 5e-6     # temp correction to n²

# --- Sellmeier functions ---
def n_y(lambda_um, T):
    n2 = A_y + B_y / (1 - C_y / lambda_um**2) - D_y * lambda_um**2
    n2 += F_temp * (T - 25)**2
    return np.sqrt(n2)

def n_z(lambda_um, T):
    n2 = A_z + B_z / (1 - C_z / lambda_um**2) - D_z / (1 - E_z / lambda_um**2) - F_z * lambda_um**2
    n2 += F_temp * (T - 25)**2
    return np.sqrt(n2)

# --- Refractive indices at each temperature ---
n_p = n_z(lambda_p, temperatures)   # Pump: z-axis
n_s = n_y(lambda_s, temperatures)   # Signal: y-axis
n_i = n_z(lambda_i, temperatures)   # Idler: z-axis

# --- Calculate wavevectors ---
k_p = 2 * np.pi * n_p / lambda_p
k_s = 2 * np.pi * n_s / lambda_s
k_i = 2 * np.pi * n_i / lambda_i

# --- Phase-matching poling period ---
Lambda = 2 * np.pi / (k_p - k_s - k_i)

# --- Normalize Λ to 10 µm at 25°C ---
idx_25C = np.abs(temperatures - 25).argmin()
Lambda_25C = Lambda[idx_25C]
Lambda_scaled = Lambda * (10 / Lambda_25C)

# --- Apply thermal expansion ---
thermal_expansion = 1 + A_exp * (temperatures - 25) + B_exp * (temperatures - 25)**2
Lambda_final = Lambda_scaled * thermal_expansion

# --- Plotting ---
plt.figure(figsize=(8, 5))
plt.plot(temperatures, Lambda_final, color='darkgreen', linewidth=2)
plt.axvline(25, color='gray', linestyle='--', linewidth=1)
plt.text(26, Lambda_final[idx_25C]+0.01, f"25°C → {Lambda_final[idx_25C]:.2f} µm", fontsize=9, color='gray')
plt.title("Poling Period vs Temperature for PPKTP (Type-II SPDC)", fontsize=13)
plt.xlabel("Temperature (°C)", fontsize=12)
plt.ylabel("Poling Period Λ (µm)", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Output poling period at 25°C ---
print(f"Poling period at 25°C (scaled): {Lambda_final[idx_25C]:.4f} µm")