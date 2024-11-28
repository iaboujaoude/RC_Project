from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# Motor 1
motor1_pin = 7 # Use the appropriate GPIO pin for Motor 1
GPIO.setup(motor1_pin, GPIO.OUT)
motor1_pwm = GPIO.PWM(motor1_pin, 1000) # Set PWM frequency for Motor 1

# Motor 2
motor2_pin = 15 # Use the appropriate GPIO pin for Motor 2
GPIO.setup(motor2_pin, GPIO.OUT)
motor2_pwm = GPIO.PWM(motor2_pin, 1000) # Set PWM frequency for Motor 2

input_pin = 12 # Use the appropriate GPIO pin for the input
GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

motor1_speed = 79.27 # Set the desired speed for motor 1 (in RPM)
motor2_speed = 100 # Set the desired speed for motor 2 (in RPM)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/turn_on")
def turn_on():
    motor1_pwm.start((motor1_speed / 100) * 100) # Start Motor 1
    motor2_pwm.start((motor2_speed / 100) * 100) # Start Motor 2
    while True:
        if GPIO.input(input_pin) == GPIO.LOW:
            motor1_pwm.ChangeDutyCycle(20)
            motor2_pwm.ChangeDutyCycle(20)
        else:
            motor1_pwm.ChangeDutyCycle((motor1_speed / 100) * 100)
            motor2_pwm.ChangeDutyCycle((motor2_speed / 100) * 100)
        time.sleep(0.5)
    return "Turned On"

@app.route("/start/<int:delay>")
def start_delayed(delay):
    if GPIO.input(motor1_pin) == GPIO.HIGH:
        return "no"
    start_after_delay(delay)
    return "ok"

@app.route("/target/<int:speed>")
def target_speed(speed):
    if GPIO.input(motor1_pin) == GPIO.HIGH:
        return "no"
    motor1_pwm.start((speed / 359) * motor1_speed)
    motor2_pwm.start((speed / 359) * motor2_speed)
    return "ok"

def start_after_delay(delay):
    time.sleep(delay)
    motor1_pwm.start((motor1_speed / 100) * 100)
    motor2_pwm.start((motor2_speed / 100) * 100)

@app.route("/turn_off")
def turn_off():
    motor1_pwm.stop()
    motor2_pwm.stop()
    return "Turned Off"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=80, debug=True)
    finally:
        GPIO.cleanup()
