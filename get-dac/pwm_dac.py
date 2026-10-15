import RPi.GPIO as GPIO
gpio_bits = [16, 20, 21, 25, 26, 17, 27, 22]
dynamic_range = 3.18



class PWM_DAC:
    def __init__(self, gpio_bits, frequency, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.frequency = frequency

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

        self.pwm = GPIO.PWM(self.gpio_bits, self.frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
            number = max(0, min(int(number), 255))
            duty = number / 255 * 100 
            self.pwm.ChangeDutyCycle(duty)
            if self.verbose:
                print(f"set_number: {number} -> duty {duty:.2f} %")

    def set_voltage(self, voltage):
        if not(0.0 <= voltage <= dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
            print("Устанавливаем 0.00 В")
            voltage = 0
        self.set_number(int(voltage/self.dynamic_range * 255))



if __name__ == "__main__":
    dac = None
    try:
        dac = PWM_DAC(12, 50, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally: 

      if dac is not None:
            dac.deinit()


