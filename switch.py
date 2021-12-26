import RPi.GPIO as GPIO
state = False
def button_callback(channel):
    state = GPIO.input(channel)
    if state==0:
        print("Botón presionado\n")
    else:
        print("Botón no presionado\n")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(13,GPIO.BOTH,callback=button_callback)
message = input("Press enter to quit\n")
GPIO.cleanup()