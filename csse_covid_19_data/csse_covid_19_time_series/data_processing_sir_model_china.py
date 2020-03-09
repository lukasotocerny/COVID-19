import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv

# Total population, N.
# N = 82000
N = 22000
# Initial number of infected and recovered individuals, I0 and R0.
# I0, R0 = 547, 0
I0, R0 = 20, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
# beta, gamma = 0.3, 0.025
beta, gamma = 0.247, 0.025
# A grid of time points (in days)
t = np.linspace(0, 60)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axis_bgcolor='#dddddd', axisbelow=True)
ax.plot(t, N-S, 'b', alpha=0.5, lw=2, label='Confirmed (Model)')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Currently sick (Model)')
# ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number')
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)

# Confirmed cases
bias = 4
def process_dataset(dataset, country, start_day, end_day):
    res = [0 for i in range(end_day-start_day-bias)]
    with open('time_series_19-covid-{}.csv'.format(dataset), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        dates = None
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            if row[1] == country:
                for i in range(bias+start_day, end_day):
                    res[i-bias-start_day] += int(row[i])
    return np.array(res)


def process_china():
    start_day = 0
    end_day = 50
    confirmed = process_dataset("Confirmed", "Mainland China", start_day, end_day)
    deaths = process_dataset("Deaths", "Mainland China", start_day, end_day)
    recovered = process_dataset("Recovered", "Mainland China", start_day, end_day)
    return confirmed, deaths, recovered, start_day, end_day

def process_italy():
    start_day = 23
    end_day = 50
    confirmed = process_dataset("Confirmed", "Italy", start_day, end_day)
    deaths = process_dataset("Deaths", "Italy", start_day, end_day)
    recovered = process_dataset("Recovered", "Italy", start_day, end_day)
    return confirmed, deaths, recovered, start_day, end_day

confirmed, deaths, recovered, start_day, end_day = process_china()


# Add China data
t = np.linspace(0, end_day-start_day, end_day-start_day-bias)
plt.scatter(t, confirmed, c='b', label='Confirmed (Actual)')
plt.scatter(t, confirmed-deaths-recovered, c='r', label='Currently sick (Actual)')

fontP = FontProperties()
fontP.set_size('small')
legend = ax.legend(loc="upper left", prop=fontP)
legend.get_frame().set_alpha(0.5)


plt.title("COVID-19 SIR model in Italy")
plt.show()