from application.config.ServerConfig import ServerConfig
from application.util.TimeUtil import *
import os


def write_error_log(log_message: str) -> None:
    """
    写入异常日志
    :param log_message: 日志信息
    :return:
    """
    log_dir: str = ServerConfig.log_dir
    log_file: str = os.path.join(log_dir, f"{now_format_date()}.error.log")
    log_message = f"{now_format_datetime()} - 错误信息 => \n {log_message}\n"
    with open(file=log_file, mode="a+", encoding="utf-8") as f:
        f.write(log_message)


def write_info_log(log_message: str) -> None:
    """
    写入信息日志
    :param log_message: 日志信息
    :return:
    """
    log_dir: str = ServerConfig.log_dir
    log_file: str = os.path.join(log_dir, f"{now_format_date()}.info.log")
    log_message = f"{now_format_datetime()} - 正常信息 => {log_message}\n"
    with open(file=log_file, mode="a+", encoding="utf-8") as f:
        f.write(log_message)
