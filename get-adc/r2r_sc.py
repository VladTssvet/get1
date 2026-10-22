import r2r_adc as r2r
import adc_plot
import time

voltage_values = []
time_values = []
duration = 3.0
dynamic_range = 3.183

if __name__ == "__main__":
    try:
        adc = r2r.R2R_ADC(dynamic_range, compare_time=0.0001, verbose=False)

        start_time = time.time()

        while (time.time() - start_time) < duration:
            v = adc.get_sc_voltage()
            t = time.time() - start_time

            voltage_values.append(v)
            time_values.append(t)

        adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

    finally:
        adc.deinit()
