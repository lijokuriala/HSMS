#!/usr/bin python3


import sys
import time
from time import strftime
import logging
import traceback

import RPi.GPIO as GPIO
sys.path.append('/usr/local/etc')
import gdoor_config as cfg

from firebase import firebase

# Firebase connection
firebase = firebase.FirebaseApplication("https://homesecuritymonitoringsystem.firebaseio.com/", None)


# Get Sensor data
def get_sensor_state(pin):
    if GPIO.input(pin):
        state = 'Open'
    else:
        state = 'Closed'

    return state


def log_sensor_data(sensor_name, state, time_string):
    # ##Write data to firebase database###
    # Format sensor data to save in key:value pairs
    sensor_data = {
        'Sensor': sensor_name,
        'State': state,
        'Time': time_string
    }
    # Post data to firebase database table
    db_save_result = firebase.post('/table_SensorStateData', sensor_data)
    return db_save_result

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
            # sensor_name = "Main Garage"
            # sensor_pin = 15

            # Configure sensor pins
            for sensor in cfg.SENSORS:
                self.logger.info("Configuring pin %d for \"%s\"", sensor['pin'], sensor['name'])
                GPIO.setup(sensor['pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                self.logger.info("Status of sensor is \"%s\"", get_sensor_state(sensor['pin']))

            # Last state of each garage door
            sensor_states = dict()

            # time.time() of the last time the garage door changed state
            time_of_last_state_change = dict()
            time_no_change = dict()

            # Get init values
            for sensor in cfg.SENSORS:
                sensor_name = sensor['name']
                sensor_states[sensor_name] = get_sensor_state(sensor['pin'])
                time_of_last_state_change[sensor_name] = time.time()
                time_no_change[sensor['name']] = 0
                # Write init values into DB
                db_save_result = log_sensor_data(sensor_name, sensor_states[sensor_name], time_of_last_state_change[sensor_name])
                self.logger.info(db_save_result)
                self.logger.info(sensor_states[sensor_name])

            while True:
                for sensor in cfg.SENSORS:
                    sensor_name = sensor['name']
                    state = get_sensor_state(sensor['pin'])
                    time_in_state = time.time() - time_of_last_state_change[sensor_name]
                    time_string = time.strftime('%Y-%b-%d %I:%M:%S %p %Z')

                    # Check if sensor state has changed
                    if sensor_states[sensor_name] != state:
                        sensor_states[sensor_name] = state
                        time_of_last_state_change[sensor_name] = time.time()
                        #  time_in_state = time.time() - time_of_last_state_change[sensor_name]
                        self.logger.info("State of \"%s\" changed to %s after %.0f sec at %s", sensor_name, state, time_in_state, time_string)

                        # ##Write data to firebase database###
                        db_save_result = log_sensor_data(sensor_name, state, time_string)
                        self.logger.info(db_save_result)
                        self.logger.info(state)

                        # Reset time_in_state
                        time_in_state = 0

                    # Calculate time since last change
                    time_no_change[sensor_name] = time.time() - time_of_last_state_change[sensor_name]
                    # self.logger.info("Time no change  %0.f sec", time_no_change)

                    # Log a message on console when no change in state of sensor
                    if int(time_no_change[sensor_name]) >= 15:
                        if int(time_no_change[sensor_name]) % 15 == 0:
                            self.logger.info("No change in status of %s for 15 seconds now #30 minutes now", sensor_name)

                            # If sensor is open for 30 minutes, log an alert into Firebase DB.
                            if state == "Open":
                                db_save_result = log_sensor_data(sensor_name, "Alert", time_of_last_state_change[sensor_name])
                                self.logger.info(db_save_result)
                                self.logger.info("Alert")

                # Wait for a minute before checking change in status
                time.sleep(1)  # 60, temporarily using 1 sec for Demo

        except KeyboardInterrupt:
            logging.critical("Terminating due to keyboard interrupt")
        except:
            logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
            logging.critical("%s", traceback.format_exc())

        GPIO.cleanup()


if __name__ == "__main__":
    HSMS().main()
