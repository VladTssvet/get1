import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    
    plt.title("Напряжение на входе АЦП от времени")
    plt.xlabel("Время, c")
    plt.ylabel("Напряжение, B")
    
    if time:
        plt.xlim(0, time[-1])
    plt.ylim(0, max_voltage)
    
    plt.grid(True)
    plt.show()

def plot_sampling_period_hist(time):
    sampling_periods = []
    for i in range(len(time) - 1):
        period = time[i + 1] - time[i]
        sampling_periods.append(period)

    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins = 50)
    
    plt.title("Распределение периодов дискретизации измерений\nпо времени на одно измерение")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    
    plt.xlim(0, 0.06)
    plt.grid(True)
    plt.show()


def plot_voltage_histogram(periods):
    plt.figure(figsize=(10, 6))
    plt.hist(periods, bins=50, color='tab:blue', edgecolor='black')
    plt.title("Распределение периодов дискретизации измерений\nпо времени на одно измерение")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    plt.grid(True)
    plt.show()

