import base64
import hashlib
import hmac
import json

from django.conf import settings


class FacebookUserIdDecoder:
    """
    FacebookUserIdDecoder
    =====================

    :request_data: request.POST
    :encoding: optional, default='utf-8'

    I have referenced this code: https://stackoverflow.com/a/48609149/3117592
    """
    secret_key = None
    signed_request = None
    encoding = None
    _user_id = None

    def __init__(self, request_data, encoding='utf-8'):
        self.secret_key = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        self.signed_request = request_data.get('signed_request')
        self.encoding = encoding

        self.start_decoding()

    def get_signed_request(self):
        assert self.signed_request is not None, (
            '`signed_request cannot be None`'
        )
        return self.signed_request

    def get_secret_key(self):
        assert self.secret_key is not None, (
            'Invalid secret_key. Set `SOCIAL_AUTH_FACEBOOK_SECRET` in project settings.'
        )
        return self.secret_key

    def get_encoding(self):
        if self.encoding is None:
            return 'utf-8'
        return self.encoding

    def parse_signed_request(self):
        return self.get_signed_request().split('.')

    def decode_payload(self, payload):
        _decoded = base64.urlsafe_b64decode(payload + "==").decode(self.get_encoding())
        _decoded = json.loads(_decoded)

        assert isinstance(_decoded, dict) and 'user_id' in _decoded.keys(), (
            'Invalid decoded payload'
        )

        return _decoded

    @staticmethod
    def decoded_sig(encoded_sig):
        return base64.urlsafe_b64decode(encoded_sig + "==")

    def expected_sig(self, payload):
        _key = bytes(self.get_secret_key(), self.get_encoding())
        _msg = bytes(payload, self.get_encoding())
        return hmac.new(_key, _msg, hashlib.sha256)

    @staticmethod
    def validate_signed(expected, decoded):
        validation = hmac.compare_digest(expected.digest(), decoded)

        assert validation is True, (
            'Invalid `signed_request`'
        )

    def set_user_id(self, decoded_payload):
        """Can use @user_id.setter"""
        user_id = decoded_payload.get('user_id')

        assert user_id is not None, (
            '`user_id` cannot be None'
        )
        self._user_id = user_id

    def start_decoding(self):
        encoded_sig, payload = self.parse_signed_request()

        expected = self.expected_sig(payload)
        decoded = self.decoded_sig(encoded_sig)
        self.validate_signed(expected, decoded)

        decoded_payload = self.decode_payload(payload)

        self.set_user_id(decoded_payload)

    def get_user_id(self):
        return self._user_id
