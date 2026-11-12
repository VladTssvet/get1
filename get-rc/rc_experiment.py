import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.186
PIN = 14
PRE_DISCHARGE = 3        # Уменьшил время, чтобы не ждать 50 секунд
CHARGE_TIME = 15         # 15 секунд на зарядку
DISCHARGE_TIME = 15      # 15 секунд на разрядку
CSV_NAME = "data.csv"    # То самое имя файла из задания

times = []
voltages = []
states = []

def record(adc, duration, state, start):
    t_end = time.time() + duration
    while time.time() < t_end:
        # Читаем без всяких "заглушек", как в твоем рабочем коде
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)
        states.append(state)

def save_csv():
    with open(CSV_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Время [с]", "Напряжение [В]"])
        for t, v in zip(times, voltages):
            writer.writerow([f"{t:.4f}", f"{v:.4f}"])
    print(f"Данные сохранены в {CSV_NAME}")

def plot():
    plt.figure(figsize=(10, 6))
    plt.plot(times, voltages, ".-", markersize=2, label="Напряжение на конденсаторе")
    plt.title("Зарядка и разрядка конденсатора")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.ylim(0, DYNAMIC_RANGE)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.savefig("graph.png")
    print("График сохранен в graph.png")

    plt.show() 

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT, initial=0)
    adc = MCP3021(DYNAMIC_RANGE)
    
    try:
        print(f"Разряжаю конденсатор {PRE_DISCHARGE} с перед началом...")
        time.sleep(PRE_DISCHARGE)
        start = time.time()

        print("Зарядка: GPIO14 = 1")
        GPIO.output(PIN, 1)
        record(adc, CHARGE_TIME, 1, start)

        print("Разрядка: GPIO14 = 0")
        GPIO.output(PIN, 0)
        record(adc, DISCHARGE_TIME, 0, start)

    except KeyboardInterrupt:
        print("\nИзмерение прервано")
    finally:
        GPIO.output(PIN, 0)
        GPIO.cleanup()
        adc.deinit()

    if times:
        print(f"Измерений: {len(times)}, частота ~{len(times) / times[-1]:.0f} Гц")
        save_csv()
        plot()
