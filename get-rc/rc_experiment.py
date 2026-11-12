import csv
import time
import os  # Модуль для работы с папками
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

print("--- ЗАПУЩЕН НОВЫЙ КОД ---")
print("Я нахожусь в папке:", os.getcwd())  # Покажет текущую папку

DYNAMIC_RANGE = 5.186
PIN = 14
PRE_DISCHARGE = 3
CHARGE_TIME = 5
DISCHARGE_TIME = 5

times = []
voltages = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=0)
adc = MCP3021(DYNAMIC_RANGE)

try:
    print("Разрядка перед стартом...")
    time.sleep(PRE_DISCHARGE)
    start = time.time()

    print("Зарядка (GPIO14 = 1)...")
    GPIO.output(PIN, 1)
    t_end = time.time() + CHARGE_TIME
    while time.time() < t_end:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)

    print("Разрядка (GPIO14 = 0)...")
    GPIO.output(PIN, 0)
    t_end = time.time() + DISCHARGE_TIME
    while time.time() < t_end:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)

    print("Собрано точек:", len(times))
    print("Начинаю сохранять данные в файл data.csv...")
    
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Время [с]", "Напряжение [В]"])
        for t, v in zip(times, voltages):
            writer.writerow([f"{t:.4f}", f"{v:.4f}"])
            
    print("Файл data.csv УСПЕШНО СОХРАНЕН!")

    print("Начинаю строить график...")
    plt.figure(figsize=(10, 6))
    plt.plot(times, voltages, color='blue')
    plt.title("Зарядка и разрядка")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.grid(True)
    
    plt.savefig("graph.png")
    print("График graph.png УСПЕШНО СОХРАНЕН!")
    print("--- РАБОТА ЗАВЕРШЕНА ---")

except Exception as e:
    print(f"\n!!! ПРОИЗОШЛА ОШИБКА: {e}") # Если что-то упадет, мы это увидим

finally:
    GPIO.output(PIN, 0)
    GPIO.cleanup()
    if 'adc' in locals():
        adc.deinit()
