from application.config.EmailConfig import EmailConfig
from zmail.server import MailServer
from httpx import Response, request
import zmail


def send_email_by_api(target_email: str, title: str, content: str) -> bool:
    """
    使用在线API发送邮件
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


def send_email(target_email: str, title: str, content: str) -> bool:
    """
    发送邮件
    :param target_email: 目标邮箱
    :param title: 邮件标题
    :param content: 邮件正文
    :return: bool
    """
    server: MailServer = zmail.server(username=EmailConfig.email_from, password=EmailConfig.email_password)
    return server.send_mail(recipients=target_email,
                            mail={
                                "subject": title,
                                "content_text": content
                            })
