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
            logging.info(("Status of door is \"%s\"", get_garage_door_state(15)))

            state = get_garage_door_state(15)
            while True:
                # Last state of each garage door
                door_states = dict()

                # time.time() of the last time the garage door changed state
                time_of_last_state_change = dict()

                door_states["MainGarage"] = get_garage_door_state(15)
                time_of_last_state_change["MainGarage"] = time.time()

                if door_states["MainGarage"] != state:
                    door_states["MainGarage"] = state
                    time_of_last_state_change["MainGarage"] = time.time()
                    self.logger.info("State changed to %s",state)

        except KeyboardInterrupt:
            logging.critical("Terminating due to keyboard interrupt")
        except:
            logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
            logging.critical("%s", traceback.format_exc())

        GPIO.cleanup()


if __name__ == "__main__":
    HSMS().main()
