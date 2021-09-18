from devices.dependencies import get_logger
from fastapi import Depends


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
        def analyse(service_logger=Depends(get_logger),):
            data = [0, 1]
            service_logger().info("test")
            if data[0] > data[1]:
                # send message pump on
                pass
            elif data[1] > data[0]:
                # send message pump off
                pass
