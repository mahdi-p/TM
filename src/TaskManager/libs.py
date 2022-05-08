"""
This module provides some helper functions for:
    Module logging: mlogger
    Pipeline logging: py_logger
    Yaml file reader and parser: get_config
"""

from typing import Dict
import time
import logging
import pathlib
import yaml


class MaxTaskSizeError(Exception):
    pass


class DuplicateTaskError(Exception):
    pass


class EmptyTaskManagerError(Exception):
    pass


class InactiveTaskError(Exception):
    pass


def mlogger(message: str = " ", level: str = "INFO") -> None:
    """
    Creates simple module logger

    Parameters:
    -----------
       message: str
            Message to be printed.
       level: str
            Default to INFO (At the moment only INFO is implemented.)
       """
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    if level == "INFO":
        print(f"[INFO - {time_string}]: {message}")


def get_config(conf_file) -> Dict:  # : pathlib.PosixPath
    """
    YAML config file parser.

    Parameters:
    -----------
        conf_file: pathlib.PosixPath:
            pathlib.PosixPath to file location.
    """

    if isinstance(conf_file, str):
        conf_file = pathlib.Path(conf_file)

    if conf_file.is_file() and conf_file.suffix == '.yaml':
        with open(conf_file, mode="r") as stream:
            conf = yaml.safe_load(stream.read())
    else:
        mlogger(f"The input file '{conf_file}' is: not valid file or does not exists.")
        return dict()
    return conf


def py_logger(name="__name__", log_path="",
              level=logging.INFO,
              formatter=logging.Formatter('[%(levelname)s - %(name)s - %(asctime)s]  %(message)s',
                                          datefmt='%m-%d-%Y %H:%M:%S')):
    """
    Creates a log and stream handler in order to create a log file for the pipeline.

    Parameters:
    -----------
        name: str
            Name of script or any other string.
        log_path: str
            Path where the logs will be collected.
        level:
            Logging level. Default to INFO.
        formatter:
            Logging formatter of type logging.Formatter
    """

    formatter = formatter
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
