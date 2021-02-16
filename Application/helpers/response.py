from flask import jsonify

# import session helpers
from .session import get_current_session


class Response:
    """Default items for api response"""
    session = None
    data = None
    errors = None
    status_code = None
    message = None
    status_message = None

    def __init__(self, session=None, status_code=200, message='', status_message=None, data=None, errors=None):
        """Set up construct values"""
        self.session = session
        self.data = data
        self.errors = errors
        self.status_message = status_message
        self.status_code = status_code
        self.message = message
        self.status_message = status_message

        """Init session for every valid user"""
        self.get_session()

        """Setup status message for every request"""
        self.set_status()

    def get_session(self):
        self.session = get_current_session(formatted=True)

    def set_status(self):
        if str(self.status_code).startswith('2'):
            self.status_message = 'success'
        elif str(self.status_code).startswith('1') or str(self.status_code).startswith('3'):
            self.status_message = 'warning'
        elif str(self.status_code).startswith('4') or str(self.status_code).startswith('5'):
            self.status_message = 'danger'
        else:
            self.status_message = 'primary'

    def send(self):
        return jsonify({
            'session': self.session,
            'status_message': self.status_message,
            'status_code': self.status_code,
            'data': self.data,
            'errors': self.errors,
            'message': self.message
        }), self.status_code
