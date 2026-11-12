import time
import csv
import adc_plot
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.0
DURATION =  100
CSV_PATH = "adc_data.csv"

# Пороги для статуса конденсатора
THRESHOLD_LOW = 0.1    # В — ниже считаем разряженным
THRESHOLD_HIGH = 4.9   # В — выше считаем заряженным

adc = MCP3021(dynamic_range=DYNAMIC_RANGE, verbose=False)

voltage_values = []
time_values = []

# Чтобы не спамить одинаковым сообщением каждые 10 мс — запоминаем последний статус
last_status = None


def update_status(voltage):
    """Печатает статус конденсатора при переходе через порог."""
    global last_status

    if voltage < THRESHOLD_LOW:
        status = "discharged"
        message = "Конденсатор разряжен"
    elif voltage > THRESHOLD_HIGH:
        status = "charged"
        message = "Заряжен"
    else:
        status = None
        message = None

    if status != last_status:
        if message is not None:
            print(message, flush=True)
        last_status = status


try:
    start_time = time.time()
    while time.time() - start_time < DURATION:
        v = adc.get_voltage()
        t = time.time() - start_time

        voltage_values.append(v)
        time_values.append(t)

        update_status(v)

        time.sleep(0.01)

    # Сохраняем данные в CSV
    with open(CSV_PATH, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "voltage_V"])
        for t, v in zip(time_values, voltage_values):
            writer.writerow([f"{t:.6f}", f"{v:.6f}"])

    print(f"Данные сохранены в {CSV_PATH} ({len(time_values)} строк)", flush=True)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()
