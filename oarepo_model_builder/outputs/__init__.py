class OutputBase:
    output_type = None

    def __init__(self, path):
        self.path = path

    def begin(self):
        raise NotImplemented()

    def finish(self):
        raise NotImplemented()
