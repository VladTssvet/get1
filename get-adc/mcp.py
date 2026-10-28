import mcp3021_driver as mcp
import adc_plot
import time

voltage_values = []
time_values = []
duration = 3.0

if __name__ == "__main__":
    try:
        adc = mcp.MCP3021(5.0, verbose=False)

        start_time = time.time()

        while (time.time() - start_time) < duration:
            v = adc.get_voltage()
            t = time.time() - start_time

            voltage_values.append(v)
            time_values.append(t)

        adc_plot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
        adc_plot.plot_sampling_period_hist(time_values)

    finally:
        adc.deinit()
