import numpy as np
import matplotlib.pyplot as plt

# Parameters

V_source = 5    # Volts
C = 1.1         # Farads
R_load = 20     # Ohms
R_switch = 1    # Ohms

t_switch = 5    # Seconds
t_end = 20      # Seconds

# Charging Phase

t_charge = np.linspace(0, t_switch, 1000)

I_source = V_source / R_switch  # Norton equivalent current source
R =  (R_load * R_switch) / (R_load + R_switch)  # Rth = Rn, taking this in parallel with the load
tau = R * C    # Time constant
V_0 = 0  # No initial voltage

Vc_charge = V_0 + I_source * R * (1 - np.exp(-t_charge / tau))
I_charge = Vc_charge / R_load

# Discharging Phase

t_discharge = np.linspace(t_switch, t_end, 1000)

R = R_load  # Switch disengages
tau = R * C    # Time constant

Vc_discharge = Vc_charge[-1] * np.exp(-(t_discharge - t_switch) / tau)
I_discharge = Vc_discharge / R_load

# Plot

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(t_charge, Vc_charge, color='blue')
plt.plot(t_discharge, Vc_discharge, color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Voltage Across Capacitor')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t_charge, I_charge, color='red')
plt.plot(t_discharge, I_discharge, color='red')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Current Across Resistor')
plt.grid(True)

plt.tight_layout()
plt.show()
