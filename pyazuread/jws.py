from .utils import isBlank
from .exception import InvalidAuthorizationToken
from jwt import InvalidTokenError, InvalidSignatureError, ExpiredSignature, DecodeError, decode, get_unverified_header

class Jws:
    
    def __init__(self, jwtString, PEMKey, options):
        self.jwtString = jwtString
        self.PEMKey = PEMKey
        self.options = options
        self.payload = {}
        self.header = {}
            
        if not jwtString or isBlank(jwtString):
            raise InvalidAuthorizationToken('jwtString must be provided')
        if not PEMKey or isBlank(PEMKey):
            raise InvalidAuthorizationToken('PEMKey must be provided')
        
        if not ('audience' in self.options and (isinstance(options.get('audience', ''), str)) or (isinstance(options.get('audience', []), list)) and len(options.get('audience', '')) > 0):
            raise InvalidAuthorizationToken('invalid audience value is provided')
        if 'algorithms' not in self.options:
            raise InvalidAuthorizationToken('algorithms is missing')
        if not isinstance(options.get('algorithms', []), list) or len(self.options.get('algorithms', [])) == 0 or (len(self.options.get('algorithms', [])) == 1 and self.options.get('algorithms', [])[0] == "none"):
            raise InvalidAuthorizationToken('algorithms must be an array containing at least one algorithm')
        
        
    def verifySub(self):
        if not isinstance(self.payload['sub'],str) or isBlank(self.payload['sub']):
            raise InvalidAuthorizationToken('invalid sub value in payload')
        if 'subject' in self.options and self.options['subject'] != self.payload['sub']:
            raise InvalidAuthorizationToken('jwt subject is invalid. expected')
        
    def verify(self):
        parts = self.jwtString.split(".")        
        if len(parts) != 3:
            raise InvalidAuthorizationToken('jwtString is malformed')
        if parts[2] == "":
            raise InvalidAuthorizationToken('signature is missing in jwtString')
        
        decodedToken = {}               
        decodedHeader = {}
        
        try:
            decodedToken = decode(self.jwtString, verify=False)
            decodedHeader = get_unverified_header(self.jwtString)
        except Exception as error:
            raise InvalidAuthorizationToken('failed to decode the token')
        
        if not decodedToken:
            raise InvalidAuthorizationToken('invalid token')
                
        self.header = decodedHeader
        self.payload = decodedToken
               
        if not isinstance(self.header['alg'], str) or isBlank(self.header['alg']) or self.header['alg'] == None or self.options['algorithms'].index(self.header['alg']) == -1:
            raise InvalidAuthorizationToken('invalid algorithm')
        
        try:
            decode(self.jwtString, self.PEMKey, verify=True, algorithms=self.header['alg'],  audience=self.options['audience'], issuer=self.options['issuer'][0])
        except (InvalidTokenError, ExpiredSignature, DecodeError)  as e:
            raise InvalidAuthorizationToken(str(e))
        
        self.verifySub()
        
        return self.payload
        
    