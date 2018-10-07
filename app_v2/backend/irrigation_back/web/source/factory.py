class Factory(object):
    """docstring for Factory"""
    def __init__(self):
        super(Factory, self).__init__()
    
    def line_status(self, line):
        return dict(
            line_id=line.id,
            status=line.status
            )