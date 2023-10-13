import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Parameters

V_thresh = 3.0  # Volts
I_thresh = 0.15 # Amps

V_source = 4.8  # Volts
R_load = 18     # Ohms
R_switch = 1    # Ohms

t_switch = 3.5    # Seconds
t_end = 100      # Seconds

# Grid search capacitances in guess_range
guess_range = [0.01,10]
max_iter = 1000

######################### OPTIMIZING C #########################

C_values = np.linspace(guess_range[0], guess_range[1], max_iter)
Cs, ts = [], []
best_values = None

# Grid search for optimal C value

for C in C_values:

    ### Charging Phase ###

    t_charge = np.linspace(0, t_switch, 1000)

    I_source = V_source / R_switch  # Norton equivalent current source
    R =  (R_load * R_switch) / (R_load + R_switch)  # Rth = Rn, taking this in parallel with the load
    tau = R * C    # Time constant
    V_0 = 0  # No initial voltage

    Vc_charge = V_0 + I_source * R * (1 - np.exp(-t_charge / tau))
    I_charge = Vc_charge / R_load

    ### Discharging Phase ###

    t_discharge = np.linspace(t_switch, t_end, 1000)

    R = R_load  # Switch disengages
    tau = R * C    # Time constant

    Vc_discharge = Vc_charge[-1] * np.exp(-(t_discharge - t_switch) / tau)
    I_discharge = Vc_discharge / R_load

    ### Metrics ###

    time_powered = 0

    try:
        Vc_charged = t_charge[np.where(np.isclose(Vc_charge, V_thresh, rtol=1e-3))[0][0]]
        Vc_discharged = t_discharge[np.where(np.isclose(Vc_discharge, V_thresh, rtol=1e-3))[0][0]]
        Vc_above_thresh = Vc_discharged - Vc_charged

        I_charged = t_charge[np.where(np.isclose(I_charge, I_thresh, rtol=1e-3))[0][0]]
        I_discharged = t_discharge[np.where(np.isclose(I_discharge, I_thresh, rtol=1e-3))[0][0]]
        I_above_thresh = I_discharged - I_charged

        time_powered = min(I_discharged, Vc_discharged) - max(I_charged, Vc_charged)

        if time_powered > I_above_thresh or time_powered > Vc_above_thresh:
            continue

    except:

        # Don't add datapoint if we can't find intersections
        continue

    if Cs and time_powered > np.max(ts):
        best_values = {
            't_charge': t_charge,
            't_discharge': t_discharge,
            'Vc_charge': Vc_charge,
            'Vc_discharge': Vc_discharge,
            'Vc_charged': Vc_charged,
            'Vc_discharged': Vc_discharged,
            'Vc_above_thresh': Vc_above_thresh,
            'I_charge': I_charge,
            'I_discharge': I_discharge,
            'I_charged': I_charged,
            'I_discharged': I_discharged,
            'I_above_thresh': I_above_thresh,
            'time_powered': time_powered
        }

    Cs.append(C)
    ts.append(time_powered)

######################### PLOTTING #########################

plt.figure(figsize=(16, 4))
plt.subplots_adjust(bottom=0.2)

### Capacitance vs. Time Powered ###

plt.subplot(1, 3, 1)

plt.plot(Cs, ts)
plt.axhline(y=np.max(ts), color='green', linestyle='--', linewidth=1)
plt.vlines(x=Cs[np.argmax(ts)], ymin=0, ymax=np.max(ts), color='green', linestyle='--', linewidth=1)
plt.xticks(list(plt.xticks()[0]) + [Cs[np.argmax(ts)]])
plt.xticks(rotation=90)
plt.yticks(list(plt.yticks()[0]) + [np.max(ts)])

plt.xlabel('Capacitance (F)')
plt.ylabel('Time (s) with Current & Voltage Constraints Met')
plt.title('Capacitance vs. Time Powered')
plt.grid(True)

### Voltage ###

plt.subplot(1, 3, 2)

plt.plot(best_values['t_charge'], best_values['Vc_charge'], color='blue')
plt.plot(best_values['t_discharge'], best_values['Vc_discharge'], color='blue')
plt.axhline(y=V_thresh, color='green', linestyle='--', linewidth=1)
plt.vlines(x=best_values['Vc_charged'], ymin=0, ymax=V_thresh, color='green', linestyle='--', linewidth=1)
plt.vlines(x=best_values['Vc_discharged'], ymin=0, ymax=V_thresh, color='green', linestyle='--', linewidth=1)
plt.xticks(list(plt.xticks()[0]) + [best_values['Vc_charged'], best_values['Vc_discharged']])
plt.xticks(rotation=90)
plt.yticks(list(plt.yticks()[0]) + [V_thresh])

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Voltage Across Capacitor')
plt.grid(True)

## Current ###

plt.subplot(1, 3, 3)

plt.plot(best_values['t_charge'], best_values['I_charge'], color='red')
plt.plot(best_values['t_discharge'], best_values['I_discharge'], color='red')
plt.axhline(y=I_thresh, color='green', linestyle='--', linewidth=1)
plt.vlines(x=best_values['I_charged'], ymin=0, ymax=I_thresh, color='green', linestyle='--', linewidth=1)
plt.vlines(x=best_values['I_discharged'], ymin=0, ymax=I_thresh, color='green', linestyle='--', linewidth=1)
plt.xticks(list(plt.xticks()[0]) + [best_values['I_charged'], best_values['I_discharged']])
plt.xticks(rotation=90)
plt.yticks(list(plt.yticks()[0]) + [I_thresh])

plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Current Across Resistor')
plt.grid(True)

print("Volt seconds: ", best_values['time_powered']*V_thresh)
print("Amp seconds: ", best_values['time_powered']*I_thresh)

plt.show()
