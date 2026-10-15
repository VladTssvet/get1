import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
r2r = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(r2r, GPIO.OUT)
dynamic_range = 3.18

def voltage_to_number(voltage):
    if not(0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.00 В")
        return 0

    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    GPIO.output(r2r, [int(element) for element in bin(number)[2:].zfill(8)])

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(r2r, 0)
    GPIO.cleanup()
