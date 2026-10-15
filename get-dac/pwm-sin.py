import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.18
signal_frequency = 20
sampling_frequency = 200

if __name__ == "__main__":
    try:
        dac = pwm.PWM_DAC(12, 5000, 3.183, True)

        start = time.time()
        while True:
            t = time.time() - start
            norm = sg.get_sin_wave_amplitude(signal_frequency, t)
            dac.set_voltage(norm * amplitude)
            sg.wait_for_sampling_period(sampling_frequency)
    finally:
        dac.deinit()