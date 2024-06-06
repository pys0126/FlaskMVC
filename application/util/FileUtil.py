"""
文件工具包
"""
from werkzeug.datastructures import FileStorage
from application.config.ServerConfig import ServerConfig


def get_size_by_file_storage(file_obj: FileStorage):
    """
    获取FileStorage对象大小
    :param file_obj: FileStorage对象
    :return:
    """
    if file_obj.content_length:
        return file_obj.content_length
    try:
        pos = file_obj.tell()
        file_obj.seek(0, 2)  # seek to end
        size = file_obj.tell()
        file_obj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass
    # in-memory file object that doesn't support seeking or tell
    return 0  # assume small enough


def verify_file_size(file_obj: FileStorage) -> bool:
    """
    验证文件大小
    :param file_obj: FileStorage对象
    :return: 大于设定值返回False，小于设定值返回True
    """
    if get_size_by_file_storage(file_obj=file_obj) > ServerConfig.file_max_size:
        return False
    return True
