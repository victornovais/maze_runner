# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# Physical Ports from Raspiberry
LEFT_MOTOR = {'pin_1': 8, 'pin_2': 10}
RIGHT_MOTOR = {'pin_1': 26, 'pin_2': 24}
SENSOR = {'TRIGGER': 13, 'ECHO': 11}

# Minimun distance in centimeters
MINIMUN_DISTANCE = 10.0


def setup_motors():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(LEFT_MOTOR['pin_1'], GPIO.OUT)
    GPIO.setup(LEFT_MOTOR['pin_2'], GPIO.OUT)

    GPIO.setup(RIGHT_MOTOR['pin_1'], GPIO.OUT)
    GPIO.setup(RIGHT_MOTOR['pin_2'], GPIO.OUT)

def setup_sensor():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(SENSOR['TRIGGER'], GPIO.OUT)
    GPIO.setup(SENSOR['ECHO'], GPIO.IN)

    GPIO.output(SENSOR['TRIGGER'], False)

def turn_left():
    GPIO.output(LEFT_MOTOR['pin_1'], GPIO.HIGH)
    GPIO.output(LEFT_MOTOR['pin_2'], GPIO.LOW)

    GPIO.output(RIGHT_MOTOR['pin_1'], GPIO.LOW)
    GPIO.output(RIGHT_MOTOR['pin_2'], GPIO.LOW)
    time.sleep(.3)
    stop()

def turn_right():
    GPIO.output(RIGHT_MOTOR['pin_1'], GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR['pin_2'], GPIO.LOW)

    GPIO.output(LEFT_MOTOR['pin_1'], GPIO.LOW)
    GPIO.output(LEFT_MOTOR['pin_2'], GPIO.LOW)
    time.sleep(.3)
    stop()

def move_forward():
    GPIO.output(LEFT_MOTOR['pin_1'], GPIO.HIGH)
    GPIO.output(LEFT_MOTOR['pin_2'], GPIO.LOW)

    GPIO.output(RIGHT_MOTOR['pin_1'], GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR['pin_2'], GPIO.LOW)

def move_backward():
    GPIO.output(LEFT_MOTOR['pin_1'], GPIO.LOW)
    GPIO.output(LEFT_MOTOR['pin_2'], GPIO.HIGH)

    GPIO.output(RIGHT_MOTOR['pin_1'], GPIO.LOW)
    GPIO.output(RIGHT_MOTOR['pin_2'], GPIO.HIGH)

def stop():
    GPIO.output(LEFT_MOTOR['pin_1'], GPIO.LOW)
    GPIO.output(LEFT_MOTOR['pin_2'], GPIO.LOW)

    GPIO.output(RIGHT_MOTOR['pin_1'], GPIO.LOW)
    GPIO.output(RIGHT_MOTOR['pin_2'], GPIO.LOW)

# Algorithm that return distance to the wall
def get_distance():
    GPIO.output(SENSOR['TRIGGER'], True)
    time.sleep(0.00001)
    GPIO.output(SENSOR['TRIGGER'], False)

    stop = 0
    start = time.time()
    while not GPIO.input(SENSOR['ECHO']):
        start = time.time()
    while GPIO.input(SENSOR['ECHO']):
        stop = time.time()

    elapsed = stop - start
    distance = (abs(elapsed) * 34300)/2

    return distance

def run_old():
	while True:
		time.sleep(.3)
		move_forward()
		distance = get_distance()
		if distance <= MINIMUN_DISTANCE:
			stop()
			while True:
				turn_left()
				distance = get_distance()
				time.sleep(.3)
				if distance > MINIMUN_DISTANCE:
					break

def can_i_move_foward():
    distance = get_distance()
    return distance > MINIMUN_DISTANCE

def run():
    while True:
        if can_i_move_foward():
            move_forward()
        else:
            stop()

            possible_choices = PATH_CHOICES

            for choice in possible_choices:
                for action in choice:
                    action()

                if can_i_move_foward():
                    break

PATH_CHOICES = [
    [turn_left],
    [turn_right, turn_right],
    [turn_right],
]

if __name__ == '__main__':
    try:
        # Vamos esperar um pouquinho
        time.sleep(10)

    	setup_motors()
    	setup_sensor()

        # Run for your life!
        run()
    except KeyboardInterrupt:
        # Cleaning GPIO ports
    	GPIO.cleanup()
    	raise
