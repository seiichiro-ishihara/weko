from datetime import datetime
import random
import string
from email_validator import validate_email
from flask import current_app
from flask_mail import Message
import hashlib

from invenio_mail.tasks import send_email

from weko_records.api import RequestMailList
from weko_records_ui.captcha import get_captcha_info
from weko_records_ui.errors import ContentsNotFoundError, InternalServerError, InvalidCaptchaError, InvalidEmailError
from weko_redis.redis import RedisConnection

def send_request_mail(item_id, mail_info):

    # Validate CAPTCHA
    captcha_key = mail_info.pop('key')
    calculation_result = mail_info.pop('calculation_result')
    if not captcha_key or not calculation_result:
        raise InvalidCaptchaError()

    redis_connection = RedisConnection()
    datastore = redis_connection.connection(db=current_app.config['CACHE_REDIS_DB'])
    captcha_answer = datastore.hgetall(captcha_key)
    encoded_calc_answer = captcha_answer.get('calculation_result'.encode())
    if encoded_calc_answer is None or calculation_result is None or \
        (int(encoded_calc_answer.decode()) != calculation_result):
        raise InvalidCaptchaError()

    # Get mail recipients
    recipients_json = RequestMailList.get_mail_list_by_item_id(item_id)
    recipients_email = [ele['email'] for ele in recipients_json]
    if not recipients_email:
        raise ContentsNotFoundError()

    # Get request mail info
    msg_sender = mail_info['from']
    msg_subject = mail_info['subject']
    msg_body = mail_info['message']

    # Validate request mail sender
    try :
        validate_email(msg_sender, check_deliverability=False)
    except Exception as ex:
        # Invalid email
        raise InvalidEmailError() # 400 Error

    # Send request mail
    msg = Message(
        msg_subject,
        sender=msg_sender,
        cc=[msg_sender],
        recipients=recipients_email,
        body=msg_body
    )

    try:
        send_email.delay(msg.__dict__)
    except Exception:
        current_app.logger.exception('Sending Email handles unexpected error.')
        raise InternalServerError()

    # Create response
    res_json = {
        "from": msg_sender,
        "to": recipients_email,
        "subject": msg_subject,
        "message": msg_body
    }
    return True, res_json


def create_captcha_image():

    expiration_seconds = current_app.config.get('WEKO_RECORDS_UI_CAPTCHA_EXPIRATION_SECONDS', 900)
    ttl = expiration_seconds - 300

    # Get CAPTCHA info
    captcha_info = get_captcha_info()

    # Create key
    current_dt = datetime.now()
    random_salt = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
    key = hashlib.sha1((current_dt.strftime('%Y/%m/%d-%H:%M:%S') + random_salt).encode()).hexdigest()

    # Set calculation answer
    redis_connection = RedisConnection()
    datastore = redis_connection.connection(db=current_app.config['CACHE_REDIS_DB'])
    datastore.hset(key, 'calculation_result', captcha_info['answer'])
    datastore.expire(key, expiration_seconds)

    # Create response
    res_json = {
        "key": key,
        'image': captcha_info['image'],
        'ttl': ttl 
    }
    return True, res_json
