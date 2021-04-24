import logging

class ConsoleWarningFormatter(logging.Formatter):
    """A logging.Formatter which prints WARNING and ERROR messages with
    a prefix of the log level colored appropriate for the log level.
    """

    def get_level_message(self, record):
        separator = ': '
        if record.levelno >= logging.ERROR:
            return colors.red(record.levelname) + separator
        if record.levelno >= logging.WARNING:
            return colors.yellow(record.levelname) + separator

        return ''

    def format(self, record):
        if isinstance(record.msg, bytes):
            record.msg = record.msg.decode('utf-8')
        message = super().format(record)
        return '{}{}'.format(self.get_level_message(record), message)
