import csv
import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

print("--- ЗАПУЩЕН НОВЫЙ КОД ---")

DYNAMIC_RANGE = 5.186
PIN = 14
PRE_DISCHARGE = 3
CHARGE_TIME = 10
DISCHARGE_TIME = 10

times = []
voltages = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=0)
adc = MCP3021(DYNAMIC_RANGE)

def safe_get_voltage():
    # Эта функция защищает от ошибок I2C (Errno 5 и 110)
    for _ in range(10): # 10 попыток
        try:
            return adc.get_voltage()
        except Exception:
            time.sleep(0.01) # Если ошибка - ждем 10 мс и пробуем снова
    return 0.0

try:
    print("Разрядка перед стартом...")
    time.sleep(PRE_DISCHARGE)
    start = time.time()

    print("Зарядка (GPIO14 = 1)...")
    GPIO.setup(PIN, GPIO.OUT) # Настраиваем на выход
    GPIO.output(PIN, 1)       # Подаем 1
    t_end = time.time() + CHARGE_TIME
    while time.time() < t_end:
        voltages.append(safe_get_voltage())
        times.append(time.time() - start)

    print("Разрядка (GPIO14 отключен)...")
    # ПЕРЕВОДИМ В РЕЖИМ ВХОДА С ПОДТЯЖКОЙ ВНИЗ (чтобы не было помех)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    
    t_end = time.time() + DISCHARGE_TIME
    while time.time() < t_end:
        voltages.append(safe_get_voltage())
        times.append(time.time() - start)

    print("Сохраняю данные...")
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Время [с]", "Напряжение [В]"])
        for t, v in zip(times, voltages):
            writer.writerow([f"{t:.4f}", f"{v:.4f}"])

    print("Строю график...")
    plt.figure(figsize=(10, 6))
    plt.plot(times, voltages, color='blue')
    plt.title("Зарядка и разрядка конденсатора")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.grid(True)
    plt.savefig("graph.png")
    print("ГОТОВО! Созданы файлы data.csv и graph.png")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    print("Очищаю пины...")
    # Сначала закрываем шину I2C, потом чистим пины
    if 'adc' in locals():
        adc.deinit()
    GPIO.cleanup()
