import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

R0 = 50.0
alpha = 4.3 * 10**(-3)
T_min = 0
T_max = 100
Ex_max = 0.1
I_max = 0.020

R_min = R0
R_max = R0 * (1 + alpha * T_max)

print(f"R(0°C) = {R_min:.4f} Ом")
print(f"R(100°C) = {R_max:.4f} Ом\n")

def R_of_T(T):
    return R0 * (1 + alpha * T)

def Ex_bridge(U, R5, R1, R3, Rd):
    return U * (Rd / (R5 + Rd) - R3 / (R1 + R3))

def bridge_equations(x):
    U_p, r5, r1, r3 = x
    return [
        U_p * (R_min / (r5 + R_min) - r3 / (r1 + r3)),
        U_p * (R_max / (r5 + R_max) - r3 / (r1 + r3)) - Ex_max,
        U_p / (r5 + R_min) - I_max,
        r1 - r5
    ]

x0 = [1.43, 21.8, 21.8, 49.9]
x_sol = fsolve(bridge_equations, x0)

U_pit, R5, R1, R3 = x_sol

print(f"Результаты расчёта:")
print(f"  Uпит = {U_pit:.4f} В")
print(f"  R5 = {R5:.4f} Ом")
print(f"  R1 = {R1:.4f} Ом")
print(f"  R3 = {R3:.4f} Ом\n")

Ex_0 = Ex_bridge(U_pit, R5, R1, R3, R_min)
Ex_100 = Ex_bridge(U_pit, R5, R1, R3, R_max)
print(f"Ex(0°C) = {Ex_0:.4f} В")
print(f"Ex(100°C) = {Ex_100:.4f} В\n")

T = np.linspace(0, 100, 200)
R_T = R_of_T(T)
Ex_real = Ex_bridge(U_pit, R5, R1, R3, R_T)
Ex_ideal = (Ex_max / (T_max - T_min)) * T
Delta = np.abs(Ex_real - Ex_ideal)
Delta_rel = (Delta / Ex_max) * 100

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0, 0].plot(T, R_T, 'b', lw=2)
axs[0, 0].set_title('Сопротивление от температуры')
axs[0, 0].set_xlabel('T, °C')
axs[0, 0].set_ylabel('R, Ом')
axs[0, 0].grid(True)

axs[0, 1].plot(T, Ex_real*1000, 'b', lw=2, label='Реальная')
axs[0, 1].plot(T, Ex_ideal*1000, 'r--', lw=1.5, label='Идеальная')
axs[0, 1].set_title('Выходное напряжение')
axs[0, 1].set_xlabel('T, °C')
axs[0, 1].set_ylabel('Ex, мВ')
axs[0, 1].legend()
axs[0, 1].grid(True)

axs[1, 0].plot(T, Delta*1000, 'g', lw=2)
axs[1, 0].set_title('Абсолютная погрешность')
axs[1, 0].set_xlabel('T, °C')
axs[1, 0].set_ylabel('Delta, мВ')
axs[1, 0].grid(True)

axs[1, 1].plot(T, Delta_rel, 'm', lw=2)
axs[1, 1].set_title('Относительная погрешность')
axs[1, 1].set_xlabel('T, °C')
axs[1, 1].set_ylabel('%')
axs[1, 1].grid(True)

plt.tight_layout()
plt.show()