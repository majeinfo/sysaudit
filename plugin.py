from include import compat as co

class Plugin(object):
    def __init__(self):
        co.debug('Plugin run')
        self.output = {}

