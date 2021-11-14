import logging

default_logger = logging.getLogger('oarepo_model_builder')


# verbosity 1 is the most serious
# verbosity 9 is the least serious

class Log:
    def __init__(self):
        self.stack = [(0, default_logger)]

    def enter(self, verbosity, fmt, *args, logger=None, **kwargs):
        if not logger:
            logger = self.stack[-1][1]
        self(verbosity, fmt, *args, logger=logger, **kwargs)
        self.stack.append((verbosity, logger))

    def leave(self, fmt=None, *args, **kwargs):
        verbosity, logger = self.stack.pop()
        if fmt:
            self(verbosity, fmt, *args, logger=logger, **kwargs)

    def __call__(self, verbosity, fmt, *args, logger=None, **kwargs):
        if not logger:
            logger = self.stack[-1][1]
        indent = '  ' * (len(self.stack) - 1)
        logger.log(logging.WARNING - verbosity, indent + fmt, *args, **kwargs)


log = Log()
