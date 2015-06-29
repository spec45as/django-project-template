# coding: utf-8

import logging

OKGREEN = '\033[92m'
ENDC = '\033[0m'
BOLD = '\033[1m'


class ColorFormatter(logging.Formatter):

    def colorize(self, message):
        return '{green}{bold}{message}{end}'.format(
            green=OKGREEN,
            bold=BOLD,
            message=message,
            end=ENDC,
        )

    def format(self, record):
        message = super(ColorFormatter, self).format(record)
        return self.colorize(message)


logger = logging.getLogger('deploy')
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setFormatter(ColorFormatter())
logger.addHandler(console)
