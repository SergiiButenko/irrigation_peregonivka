from devices.dependencies import get_logger


class CesspollRelaySensor1:
    LOGGER = get_logger()

    class WaterLevel:
        def analyse():
            data = [0, 1]

            if data[0] > data[1]:
                # send message level higher
                pass
            elif data[1] > data[0]:
                # send message level lower
                pass

    class PumpStarter:
        def analyse():
            data = [0, 1]

            if data[0] > data[1]:
                # send message pump on
                pass
            elif data[1] > data[0]:
                # send message pump off
                pass
