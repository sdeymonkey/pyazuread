import jwt
from .metadata import Metadata
from .constants import Constants
from .utils import (concatUrl, getLibraryProduct, getLibraryProductParameterName, getLibraryVersion, getLibraryVersionParameterName, isBlank, is_valid_url)
from .jws import Jws

# It takes a token and validates it against Azure AD
class Baarerstrategy:
    
    def __init__(self, options: dict, token) -> None:        
        """
        The function is used to initialize the OAuthBearerStrategy class
        
        :param options: dict
        :type options: dict
        :param token: The token that was passed in the Authorization header
        """
        self.name = 'oauth-bearer'        
        if not options:
            raise Exception("options is required")
        self._options = options
        self.token = token
        
        if 'clockSkew' in self._options and (not isinstance(self._options.get('clockSkew', 0), int) or self._options.get('clockSkew', 0) < 0 or self._options.get('clockSkew', 0) % 1 != 0):
            raise Exception("clockSkew must be a positive integer")
        if 'clockSkew' not in self._options:
            self._options['clockSkew'] = Constants.CLOCK_SKEW
        if self._options.get('passReqToCallback', False) != True:
            self._options['passReqToCallback'] = False
        if self._options.get('validateIssuer', True) != False:
            self._options['validateIssuer'] = True
        if self._options.get('allowMultiAudiencesInToken', False) != True:
            self._options['allowMultiAudiencesInToken'] = False
        
        if 'audience' in self._options and isinstance(self._options.get('audience', ""), str):
            self._options['audience'] = [self._options['audience']]
        elif 'audience' not in self._options or not isinstance(self._options.get('audience', ""), list) or len(self._options.get('audience', "")) == 0:
            self._options['audience'] = [self._options.get("clientID", ""), "spn:{}".format(self._options.get("clientID", ""))]
        
        self._options['isB2C'] = False
        
        if isBlank(self._options.get("issuer", "")):
            self._options['issuer'] = None
        if 'issuer' in self._options and isinstance(self._options.get('issuer', ""), list) and  len(self._options.get('issuer', "")) == 0:
            self._options['issuer'] = None
        if 'issuer' in self._options and not isinstance(self._options.get('issuer', ""), list):
            self._options['issuer'] = [self._options['issuer']]
        
        if 'clientID' not in self._options or isBlank(self._options.get("clientID", "")):
            raise Exception("clientID cannot be empty")
        
        if 'identityMetadata' not in self._options or is_valid_url(self._options.get('identityMetadata', '')) == None:
            raise Exception("identityMetadata must be provided and must be a https url")
                
        if 'scope' in self._options and (not isinstance(self._options.get('scope', []), list) or len(self._options['scope']) == 0):
            raise Exception("scope must be a non-empty array")
        
        self._options['_isCommonEndpoint'] = True if "/common/" in self._options['identityMetadata'] else False
                
        

    def verify(self):
        """
        It takes the tenantIdOrName and the tenantId from the options and authenticates the strategy
        :return: The return value is a dictionary with the following keys:
        """
        return self.authenticateStrategy({'tenantIdOrName': self._options['tenentId']})
        
    def jwtVerify(self, token, metadata, metadataCls):
        """
        It verifies the JWT token.
        
        :param token: The JWT token to be verified
        :param metadata: The metadata object that contains the public key
        :param metadataCls: This is the class that contains the public key for the JWT token
        :return: The Jws class is being returned.
        """
        decoded = None        
        try:
            decoded = jwt.get_unverified_header(token)
        except (jwt.DecodeError, Exception) as error:
            print("JWT token decode error")
        
        pemKey = None
        if decoded == None:
            raise Exception("Invalid JWT token")
        
        try:
            if 'x5t' in decoded:
                pemKey = metadataCls.generateOidcPEM(decoded['x5t'])
            elif 'kid' in decoded:
                pemKey = metadataCls.generateOidcPEM(decoded['kid'])
            else:
                raise Exception("Invalid Azure JWT token.")
        except Exception as e:
            raise Exception("Invalid Azure JWT token.")
       
        return Jws(token, pemKey, metadata).verify()
        

    def authenticateStrategy(self, options: dict):
        """
        It takes the token from the request body, splits it into two parts, and then verifies the second
        part using the JWT library
        
        :param options: dict
        :type options: dict
        :return: The return value is a dictionary with the following keys:
        """
        params = {}
        optionsToValidate = {}
        tenantIdOrName = options.get('tenantIdOrName') if options else ''
        params['metadataurl'] = concatUrl(self._options.get('identityMetadata'), {getLibraryProductParameterName(): getLibraryProduct(), getLibraryVersionParameterName(): getLibraryVersion()})
        
        if self._options['_isCommonEndpoint'] == False and not isBlank(tenantIdOrName):
            tenantIdOrName = None
        
        if self._options['_isCommonEndpoint'] and not isBlank(tenantIdOrName):
            params['metadataurl'] = params['metadataurl'].replace("/common/", f"/{tenantIdOrName}/")
            
        if self._options['_isCommonEndpoint'] and self._options['validateIssuer'] and (not self._options['issuer'] and isBlank(tenantIdOrName)):
            raise Exception("issuer or tenantIdOrName must be provided in order to validate issuer on common endpoint")
       
        metadataCls = Metadata(params['metadataurl'], 'oidc', self._options)
        loadMetadata = metadataCls.fetch()
        params['metadata'] = loadMetadata
        
        if self._options['validateIssuer'] and not self._options['issuer']:
            optionsToValidate['issuer'] = params['metadata']['oidc']['issuer']
        else:
            optionsToValidate['issuer'] = self._options['issuer']
        
        optionsToValidate['algorithms'] = params['metadata']['oidc']['algorithms']        
        optionsToValidate['audience'] = self._options['audience']
        optionsToValidate['validateIssuer'] = self._options['validateIssuer']
        optionsToValidate['allowMultiAudiencesInToken'] = self._options['allowMultiAudiencesInToken']
        optionsToValidate['ignoreExpiration'] = True
        optionsToValidate['clockSkew'] = self._options['clockSkew']
        
        if self._options['scope']:
            optionsToValidate['scope'] = self._options['scope']            
        optionsToValidate['isAccessToken'] = True
        
        if isBlank(self.token):
            raise Exception("token should be passed in request body")
        auth_components = self.token.split(" ")
        
        if len(auth_components) == 2 and auth_components[0].lower() == 'bearer':
            
            token = auth_components[1]
            
            if isBlank(token):
                raise Exception("token is not found")
            
            return self.jwtVerify(token, optionsToValidate, metadataCls)
        return {}
            
        
