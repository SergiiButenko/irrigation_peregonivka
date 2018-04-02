import logging
import time
from helpers import sqlite_database as database
from helpers.common import *
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
from controllers import remote_controller as remote_controller

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)


SENSORS = {}
LINES = {}


def setup_sensors_datalogger():
    try:
        lines = database.select(database.QUERY[mn()])
        logging.info(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            SENSORS[key] = {'id': row[0],
                          'type': row[1],
                          'base_url': row[2]}

        logging.info(SENSORS)
    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all sensors. {0}".format(e))


def setup_lines_datalogger():
    try:
        lines = database.select(database.QUERY[mn()])
        for row in lines:
            key = row[0]

            LINES[key] = {'id': row[0],
                          'moisture_id': row[1]}

        logging.info(LINES)
    except Exception as e:
        logging.error("Exceprion occured when trying to get settings for all branches. {0}".format(e))


def inverse(val):
    logging.info('   not inversed value {0}'.format(val))
    return round(100 - val, 2)


# For get function name intro function. Usage mn(). Return string with current function name. Instead 'query' will be QUERY[mn()].format(....)
def moisture_sensors():
    GPIO.output(15, GPIO.HIGH)
    logging.info("Getting moisture:")
    try:
        value = 0
        for line_id, line in LINES.items():
            mcp_line = line['moisture_id']
            # The read_adc function will get the value of the specified channel (0-7).
            logging.info('Reading from {0} line...'.format(mcp_line))
            avr = 0
            for i in range(11):
                # 0 - 100%
                # 1 - 0%
                value = round( ((100 * mcp.read_adc(mcp_line)) / 1023), 2)
                val = inverse(value)
                avr = avr + val
                logging.info('   value {0}'.format(val))
                time.sleep(0.5)

            avr = round(avr / 10, 4)
            logging.info('Avr value {0}'.format(avr))

            database.update(database.QUERY[mn()].format(line_id, avr))
    except Exception as e:
        logging.error(e)
    else:
        logging.info("Done!")
    finally:
        GPIO.output(15, GPIO.LOW)


def temp_sensors():
    try:
        logging.info("Getting temperature:")
        for sensor_id, sensor in SENSORS.items():
            if sensor['type'] == 'air_sensor':
                response = remote_controller.air_sensor(sensor_id)
                logging.info("Air temp: {0}".format(str(response)))
                database.update(database.QUERY[mn() + '_air'].format(
                                                            response[sensor_id]['id'], 
                                                            response[sensor_id]['air_temp'], 
                                                            response[sensor_id]['air_hum']))
            elif sensor['type'] == 'ground_sensor':
                response = remote_controller.ground_sensor(sensor_id)
                logging.info("Ground temp: {0}".format(str(response)))
                database.update(database.QUERY[mn() + '_ground'].format(response[sensor_id]['id'], response[sensor_id]['ground_temp']))
    except Exception as e:
        logging.error(e)
    else:
        logging.info("Done!")
    finally:
        pass

if __name__ == "__main__":
    setup_sensors_datalogger()
    setup_lines_datalogger()

    moisture_sensors()
    temp_sensors()

# while True:
#     # Read all the ADC channel values in a list.
#     values = [0]*8
#     for i in range(8):
#         # The read_adc function will get the value of the specified channel (0-7).
#         values[i] = mcp.read_adc(i)
#     # Print the ADC values.
#     print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
#     # Pause for half a second.
#     time.sleep(0.5)
