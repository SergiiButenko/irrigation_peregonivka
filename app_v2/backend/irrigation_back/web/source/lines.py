from smart_sys.common.database import Database
from smart_sys.irrigation.source.line import Line
from smart_sys.irrigation.source.lines import Lines
from smart_sys.irrigation.source.factory import Factory 


class Lines(object):
    """docstring for Lines"""
    def __init__(self,):
        super(Lines, self).__init__()

    @property
    def list(self):
        return Database().get_all_lines()
