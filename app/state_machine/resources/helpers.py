import logging

logger = logging.getLogger('actuator')


def get_device_IP_by_line_id(line_id):
    device_id = database.get_device_id_by_line_id(line_id)
    logger.info(f"device_id: {device_id}")
    device = database.get_device_ip(device_id)
    logger.info(f"device: {device}")
    
    if device['last_known_ip'] is None:
        raise ValueError(
            f"No IP found for device id:line_id '{device_id}:{line_id}'")

    _updated = convert_to_datetime(device['updated'])
    if _updated + timedelta(minutes=ACTIVE_IP_INTERVAL_MINUTES) < datetime.now():
        raise Exception(
            f"IP '{device['last_known_ip']}' is outdated for device id:line_id '{device_id}:{line_id}'")

    return device['last_known_ip']
