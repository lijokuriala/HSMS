#!/usr/bin python3


import sys
import time
from time import strftime
import logging
import traceback

import RPi.GPIO as GPIO

from firebase import firebase

# Firebase connection
firebase = firebase.FirebaseApplication("https://homesecuritymonitoringsystem.firebaseio.com/", None)


# Get Sensor data
def get_garage_door_state(pin):
    if GPIO.input(pin):
        state = 'Open'
    else:
        state = 'Closed'

    return state


class HSMS:
    """ Main functions of HSMS"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def main(self):

        try:
            # Set up logging
            log_fmt = '%(asctime)-15s %(levelname)-8s %(message)s'
            log_level = logging.INFO
            # Log to a real terminal stdout
            logging.basicConfig(format=log_fmt, level=log_level)

            # Banner
            self.logger.info("==========================================================")
            self.logger.info("HSMS starting")

            # Use Raspberry Pi board pin numbers
            self.logger.info("Configuring global settings")
            GPIO.setmode(GPIO.BOARD)

            # For time being using only one sensor
            # Update and change this to a dynamic list later
            sensor_name = "MainGarage"
            sensor_pin = 15

            # Configure sensor pins
            self.logger.info("Configuring pin %d for \"%s\"", 15, sensor_name)
            GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.logger.info("Status of door is \"%s\"", get_garage_door_state(sensor_pin))

            # Last state of each garage door
            door_states = dict()

            # time.time() of the last time the garage door changed state
            time_of_last_state_change = dict()

            # Get init values
            state = get_garage_door_state(sensor_pin)
            time_of_last_state_change[sensor_name] = time.time()

            status_countdown = 5

            while True:
                door_states[sensor_name] = get_garage_door_state(sensor_pin)

                if door_states[sensor_name] != state:
                    state = door_states[sensor_name]
                    time_in_state = time.time() - time_of_last_state_change[sensor_name]
                    timestring = time.strftime('%Y-%b-%d %I:%M:%S %p %Z')
                    self.logger.info("State of \"%s\" changed to %s after %.0f sec at %s", sensor_name, state,
                                     time_in_state, timestring)

                    # ##Write data to firebase database###
                    # Format sensor data to save in key:value pairs
                    sensor_data = {
                        'Sensor': sensor_name,
                        'State': state,
                        'Time': timestring
                    }
                    # Post data to firebase database table
                    db_save_result = firebase.post('/table_SensorStateData', sensor_data)
                    self.logger.info(db_save_result)

                    # Reset time_in_state
                    time_in_state = 0
                    time_of_last_state_change[sensor_name] = time.time()

                status_countdown -= 1
                if status_countdown <= 0:
                    self.logger.info("No change in status for 15 seconds now #30 minutes now")
                    status_countdown = 15   # 1800=30mins

                # Wait for a second before checking change in status
                time.sleep(1)

        except KeyboardInterrupt:
            logging.critical("Terminating due to keyboard interrupt")
        except:
            logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
            logging.critical("%s", traceback.format_exc())

        GPIO.cleanup()


if __name__ == "__main__":
    HSMS().main()
