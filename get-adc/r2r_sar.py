import r2r_adc
import adc_plot
import time

voltage_values = []
time_values = []
duration = 3.0

if __name__ == "__main__":
    try:
        adc = r2r_adc.R2R_ADC(3.183, compare_time=0.001, verbose=False)

        start_time = time.time()

        while (time.time() - start_time) < duration:
            v = adc.get_sar_voltage()
            t = time.time() - start_time

            voltage_values.append(v)
            time_values.append(t)

        adc_plot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
        
        adc_plot.plot_voltage_histogram(voltage_values, adc.dynamic_range)

    finally:
        adc.deinit()
