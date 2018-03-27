import logging
import time
from helpers import sqlite_database as database
from helpers.common import *
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


def inverse(val):
    logging.info('   not inversed value {0}'.format(val))
    return round(1 - val, 2)


# For get function name intro function. Usage mn(). Return string with current function name. Instead 'query' will be QUERY[mn()].format(....)
def moisture_sensors():
    try:
        value = 0
        for x in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            logging.info('Reading from {0} line...'.format(i))
            avr = 0
            for i in range(0, 11):
                # 0 - 100%
                # 1 - 0%
                value = mcp.read_adc(x)
                val = inverse(value)
                avr = avr + val
                logging.info('   value {0}'.format(val))
                time.sleep(1)

            avr = round(avr / 10, 4)
            logging.info('Avr value {0}'.format(avr))

            database.update(database.QUERY[mn()].format(x, avr))

            time.sleep(1)
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    moisture_sensors()


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
