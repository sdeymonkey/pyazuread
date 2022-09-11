# This class is used to raise an exception when the authorization token is invalid
class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__('Invalid authorization token: ' + details)
        
