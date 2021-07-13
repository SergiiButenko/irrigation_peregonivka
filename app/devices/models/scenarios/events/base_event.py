class BaseEvent:

    def __init__(self, conditions, actions) -> None:
        self.conditions = conditions
        self.actions = actions

    def parse_obj(self, inpur_object: dict):
        pass

    def analyse(self):
        for condition in self.conditions:
            if condition.analyse() is False:
                raise Exception(f"Condition {condition} blocks execution")

    def _execute(self):
        for action in self.actions:
            action.execute

    def try_execute(self):
        self.analyse()
        self.execute()

        raise Exception("Cannot execute. Didn't pass analysis step")
