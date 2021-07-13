import yaml


class Scenario:

    def __init__(self, path: str) -> None:
        self.path = path
        self.device_id = None
        self.components = None

    def parse_scenario(self) -> dict:
        with open(self.path, "r") as f:
            _document = yaml.load(f, yaml.FullLoader)
            yaml.add_path_resolver

            return _document
        
    def _get_events(self, document: dict):
        _components = document[self.device_id]
        for _component in _components:
            _events = _component['events']


#         {
#     "cesspoll_relay_sensor1": {
#         "1": {
#             "events": [
#                 {
#                     "register_data": [
#                         {
#                             "conditions": {
#                                 "check_data": {
#                                     "data_path": "data/cesspoll",
#                                     "data_condition": "> 1",
#                                     "data_delta": 1
#                                 }
#                             },
#                             "actions": [
#                                 {
#                                     "send_message": {
#                                         "message": "Рівень води в септику вище норми",
#                                         "to": "-8u2y3984y9283y",
#                                         "when": "imidiatelly"
#                                     }
#                                 }
#                             ]
#                         },
#                         {
#                             "conditions": [
#                                 {
#                                     "value_path": "data/cesspoll",
#                                     "value_condition": "< 1",
#                                     "value_delta": 1
#                                 }
#                             ],
#                             "actions": [
#                                 {
#                                     "send_message": {
#                                         "message": "Рівень води в септику в нормі",
#                                         "to": "-8u2y3984y9283y"
#                                     }
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             ]
#         },
#         "2": {
#             "events": [
#                 {
#                     "register_data": [
#                         {
#                             "conditions": {
#                                 "check_data": {
#                                     "data_path": "data/cesspoll",
#                                     "data_condition": "> 1",
#                                     "data_delta": 1
#                                 }
#                             },
#                             "actions": [
#                                 {
#                                     "send_message": {
#                                         "message": "Насос увімкнений",
#                                         "to": "-8u2y3984y9283y",
#                                         "when": "imidiatelly"
#                                     }
#                                 }
#                             ]
#                         },
#                         {
#                             "conditions": [
#                                 {
#                                     "value_path": "data/cesspoll",
#                                     "value_condition": "< 1",
#                                     "value_delta": 1
#                                 }
#                             ],
#                             "actions": [
#                                 {
#                                     "send_message": {
#                                         "message": "Насос виключений",
#                                         "to": "-8u2y3984y9283y"
#                                     }
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             ]
#         }
#     }
# }