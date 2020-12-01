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


class main_hsms:
    """ Main functions of HSMS"""

    def main(self):

        try:
            # Configure sensor pis
            #           for gdoor in gdoorcfg.GARAGE_DOORS:
            #                self.logger.info("Configuring pin %d for \"%s\"", gdoor['pin'], gdoor['name'])
            self.logger.info("Status of door is \"%s\"", get_garage_door_state(15))
            logging.info(("Status of door is \"%s\"", get_garage_door_state(15)))

        except KeyboardInterrupt:
            logging.critical("Terminating due to keyboard interrupt")
        except:
            logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
            logging.critical("%s", traceback.format_exc())
