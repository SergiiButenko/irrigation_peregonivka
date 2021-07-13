import yaml

yaml.add_path_resolver('!register_data', ['RegisterData'], list)

with open("/home/sbutenko/repos/home/irrigation_peregonivka/app/devices/scenarios_library/cesspoll_relay_sensor1.yaml", "r") as f:
    print(yaml.load(f, yaml.FullLoader))
