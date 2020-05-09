#!/usr/bin/python3

from gpiozero import PWMLED, Button
from signal import pause, signal, SIGTERM
from time import sleep
from rpi_lcd import LCD
from threading import Thread
import smbus


def cleanup(signum, frame):
    exit(1)


def operate_pattern():
    global delay
    while True:

        value = pot_value(0)

        for i in array1:
            i.value = value / 256
            sleep(delay)
            i.off()

        for i in array2:
            i.value = value / 256
            sleep(delay)
            i.off()

        button.when_pressed = pattern_speed
        pattern_brightness()


def pattern_speed():
    global delay, speed_percent

    if delay >= 0.5:
        delay = 0.1
        speed_percent = 100
    else:
        delay += 0.1
        speed_percent -= 20

    lcd.text('Speed:' + ' {:1}'.format(speed_percent) + '%', 1, 'left')


def pot_value(input):
    bus.write_byte(0x48, input)
    bus.read_byte(0x48)
    return bus.read_byte(0x48)


def pattern_brightness():
    global bright_percent

    value = pot_value(0)

    bright_percent = value / 2.56

    lcd.text('Brightness:'+' {:1}'.format(int(bright_percent))+'%', 2, 'left')

    sleep(0.25)


try:
    signal(SIGTERM, cleanup)

    lcd = LCD()
    button = Button(21)
    lred = PWMLED(5)
    lgreen = PWMLED(6)
    blue = PWMLED(13)
    rgreen = PWMLED(19)
    rred = PWMLED(26)

    bus = smbus.SMBus(1)
    delay = 0.1
    speed_percent = 100

    array1 = [lred, lgreen, blue, rgreen, rred]
    array2 = [rred, rgreen, blue, lgreen, lred]

    lcd.text('Speed: 100%', 1, 'left')
    lcd.text('Brightness: 100%', 2, 'left')

    pattern = Thread(target=operate_pattern, daemon=True)
    pattern.start()

    pause()

except KeyboardInterrupt:
    exit(1)

finally:
    lred.close()
    lgreen.close()
    blue.close()
    rgreen.close()
    rred.close()
    lcd.clear()
