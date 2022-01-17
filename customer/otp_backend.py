
import time
import uuid

from requests import post
from django.conf import settings
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

cache = caches['default']


class OTPBackend(object):

    def __init__(self, key):
        self.key = str(key)
        if not self.key:
            raise ValidationError(_('Invalid phone or email'))
        self.otp = cache.get(self.key, None)

    def __update__(self):
        cache.set(self.key, self.otp)

    def send_otp(self, test=False):
        if not self.otp:
            self.otp = {
                'code': self.generate_otp(),
                'retries': 0,
                'sent': 0,
                'created': time.time()
            }
            self.__update__()
        elif self.otp['sent'] > settings.OTP_MAX_RESEND:
            raise ValidationError(_(f'Too many retries, Please try after {settings.OTP_TIMEOUT} minutes'))
        # self.__send_message__()
        self.otp['sent'] = self.otp['sent'] + 1
        self.__update__()
        if settings.DEBUG:
            print(self.otp['code']) # noqa
        if not test:
            self.send_message()

    def validate_otp(self, code):
        assert self.otp, _("OTP not generated fot given number")
        if self.otp['retries'] > settings.OTP_MAX_RETRY:
            raise ValidationError(_(f'Too many attempts, Please try after {settings.OTP_TIMEOUT} minutes'))

        if code == self.otp['code']:
            cache.delete(self.key)
            return True
        else:
            self.otp['retries'] = self.otp['retries'] + 1
            self.__update__()
            return False

    def generate_otp(self):
        return str(uuid.uuid4().int % (10 ** settings.OTP_NUMBER_OF_DIGITS)).zfill(settings.OTP_NUMBER_OF_DIGITS)

    def send_message(self):
        data = {
            "source": "AD-EngageSp",
            "destination": [
                self.key
            ],
            "text": f"Your otp for Engage Sport store is {self.otp['code']}"
        }
        url = 'http://dotline.brandmaster.ae/API/SendBulkSMS'
        header = {"Authorization": "Basic ZW5nYWdlcHI6NlBIcXVnbVQ="}
        resp = post(url, headers=header, json=data)
        resp_json = resp.json()
        if resp_json[0]['Description'] != "Success":
            raise Exception('Message sending failed')
