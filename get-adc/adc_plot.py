import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    
    plt.title("Напряжение на входе АЦП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    
    if time:
        plt.xlim(0, time[-1])
    plt.ylim(0, max_voltage)
    
    plt.grid(True)
    plt.show()
