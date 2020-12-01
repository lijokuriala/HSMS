#!/usr/bin python3


import sys
import time
import logging
import traceback

import RPi.GPIO as GPIO


# import gdoor_config as gdoorcfg


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

            if sys.stdout.isatty():
                # Connected to a real terminal - log to stdout
                logging.basicConfig(format=log_fmt, level=log_level)
            else:
                # Background mode - log to file
                logging.basicConfig(format=log_fmt, level=log_level, filename="testlog")

            # Banner
            self.logger.info("==========================================================")
            self.logger.info("HSMS starting")

            # Use Raspberry Pi board pin numbers
            self.logger.info("Configuring global settings")
            GPIO.setmode(GPIO.BOARD)
            # Configure sensor pis
            self.logger.info("Configuring pin %d for \"%s\"", 15, "MainGarage")
            GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.logger.info("Status of door is \"%s\"", get_garage_door_state(15))

            # Last state of each garage door
            door_states = dict()

            # time.time() of the last time the garage door changed state
            time_of_last_state_change = dict()

            name = "MainGarage"

            # Get init values
#            door_states[name] = get_garage_door_state(15)
            state = get_garage_door_state(15)
            time_of_last_state_change[name] = time.time()

            while True:
                door_states[name] = get_garage_door_state(15)

                if door_states[name] != state:
                    state = door_states[name]
                    time_of_last_state_change[name] = time.time()
                    self.logger.info("State changed to " + state)

                    # Reset time_in_state
                    time_in_state = 0
                time.sleep(1)

        except KeyboardInterrupt:
            logging.critical("Terminating due to keyboard interrupt")
        except:
            logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
            logging.critical("%s", traceback.format_exc())

        GPIO.cleanup()


if __name__ == "__main__":
    HSMS().main()
