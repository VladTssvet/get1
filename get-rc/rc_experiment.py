import RPi.GPIO as GPIO
import r2r_adc
import adc_plot
import time
import csv

PIN_RC = 17
DURATION = 3.0
DYNAMIC_RANGE = 3.183

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_RC, GPIO.OUT, initial=0)
        
        adc = r2r_adc.R2R_ADC(DYNAMIC_RANGE, compare_time=0.001, verbose=False)
        
        time_values = []
        voltage_values = []
        
        print("Зарядка конденсатора...")
        GPIO.output(PIN_RC, 1)
        start_time = time.time()
        
        while (time.time() - start_time) < DURATION:
            v = adc.get_sar_voltage()
            t = time.time() - start_time
            voltage_values.append(v)
            time_values.append(t)
            
        print("Разрядка конденсатора...")
        GPIO.output(PIN_RC, 0)
        start_time = time.time()
        
        while (time.time() - start_time) < DURATION:
            v = adc.get_sar_voltage()
            t = time.time() - start_time + DURATION
            voltage_values.append(v)
            time_values.append(t)
            
        print("Сохранение в data.csv...")
        with open('data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Время [с]', 'Напряжение [В]'])
            for t, v in zip(time_values, voltage_values):
                writer.writerow([f"{t:.4f}", f"{v:.4f}"])
                
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
        
    finally:
        GPIO.output(PIN_RC, 0)
        GPIO.cleanup()
        adc.deinit()
