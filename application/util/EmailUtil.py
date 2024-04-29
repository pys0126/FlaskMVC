from httpx import Response, request


def send_email(target_email: str, title: str, content: str) -> bool:
    """
    发送邮件
    :param target_email: 目标邮箱
    :param title: 邮件标题
    :param content: 邮件正文
    :return: bool
    """
    try:
        response: Response = request(method="POST", url="https://api.mu-jie.cc/email", json={
            "to": target_email,
            "title": title,
            "content": content
        })
        if response.json().get("code") == 200:
            return True
    except Exception:
        return False
