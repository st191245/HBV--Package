from HBV.User_config import *


def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger to log messages to a specified log file with the given logging level.

    This function creates a logger object with a file handler, sets the logging level,
    and attaches a formatter to structure the log messages. The log file stores all
    the logged messages.

    :param name: Name of the logger (e.g., 'action', 'warning', 'error').
    :param log_file: Path to the log file where messages should be saved.
    :param level: The minimum severity level of messages to be logged. Default is INFO.
    :return: A logger object configured with the specified settings.
    """
    # Create a file handler that logs messages to the specified log file with UTF-8 encoding.
    handler = logging.FileHandler(log_file, encoding='utf-8')

    # Set up a formatter that defines the format of the log messages.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Create a logger object with the specified name.
    logger = logging.getLogger(name)

    # Set the logging level for the logger (e.g., INFO, WARNING, ERROR).
    logger.setLevel(level)

    # Add the handler to the logger so that it writes to the log file.
    logger.addHandler(handler)

    return logger  # Return the configured logger object.


# Create loggers for different purposes: action, warning, and error logs.
action_logger = setup_logger('action', 'actions.log', logging.INFO)  # For general actions and information.
warning_logger = setup_logger('warning', 'warnings.log', logging.WARNING)  # For warning messages.
error_logger = setup_logger('error', 'errors.log', logging.ERROR)  # For error messages.
