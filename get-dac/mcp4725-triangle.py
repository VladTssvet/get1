import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 2.0
signal_frequency = 10
sampling_frequency = 500


if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(4.2, 0x61, False)

        start = time.time()
        while True:
            t = time.time() - start
            norm = sg.get_triangle_wave_amplitude(signal_frequency, t)
            dac.set_voltage(norm * amplitude)
            sg.wait_for_sampling_period(sampling_frequency)

    finally:
        dac.deinit()
