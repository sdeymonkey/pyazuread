"""**
 * @author [Suman Dey]
 * @email [sdey@surveymonkey.com]
 * @create date 2022-09-10 12:53:04
 * @modify date 2022-09-10 12:53:04
 * @desc [description]
 *"""
 
import requests
from .utils import isBlank
from .jwksutils import rsa_pem_from_jwk

# It takes a URL, and returns a dictionary of metadata
class Metadata:
    
    def __init__(self, url: str, authtype: str, options: dict) -> None:
        """
        The function takes in a url, authtype, and options, and if the url is not found, it raises an
        error. If the authtype is not oidc, it raises an error. If the url is found, it sets the url,
        metadata, authtype, and oidc to the function
        
        :param url: The URL of the OIDC provider
        :type url: str
        :param authtype: The type of authentication to use. Currently, only "oidc" is supported
        :type authtype: str
        :param options: dict
        :type options: dict
        """
        if not url:
            raise "URL not found"
        
        if authtype and authtype != "oidc":
            raise Exception("Invalid authtype. authtype must be 'oidc'")
        
        self.url = url
        self.metadata = None
        self.authtype = authtype
        self.oidc = {}
        

    def generateOidcPEM(self, kid):
        """
        If the kid is not blank, and the keys are not blank, and the key's n and e are not blank, then
        return the public key
        
        :param kid: The key ID of the public key you want to use to verify the signature
        :return: A public key in PEM format.
        """
        keys = self.oidc['keys'] if self.oidc and isinstance(self.oidc['keys'], list) else None
        pubKey = None
        foundKey = False
        
        if isBlank(kid):
            Exception("kid is missing")
        
        if not keys:
            Exception("keys is missing")
            
        for key in keys:
            if key['kid'] != kid:
                continue            
            if not key['n']:
                continue            
            if not key['e']:
                continue
            pubKey = rsa_pem_from_jwk({'n': key['n'], 'e': key['e']})
            foundKey = True
            return pubKey
            

        
    def updateOidcMetadata(self, doc) -> dict:
        """
        It takes the metadata from the OpenID Connect provider and updates the `oidc` dictionary with
        the relevant information
        
        :param doc: The metadata document
        :return: A dictionary with a key of 'oidc' and a value of the oidc dictionary.
        """
        oidc = {}
        oidc['algorithms'] = doc.get('id_token_signing_alg_values_supported', '')
        oidc['authorization_endpoint'] = doc.get('authorization_endpoint', '')
        oidc['end_session_endpoint'] = doc.get('end_session_endpoint', '')
        oidc['issuer'] = doc.get('issuer', '')
        oidc['token_endpoint'] = doc.get('token_endpoint', '')
        oidc['userinfo_endpoint'] = doc.get('userinfo_endpoint', '')
        
        jwksUri = doc.get('jwks_uri', '')
        req = requests.get(url=jwksUri)
        if req.status_code == 200:
            oidc['keys'] = req.json()['keys']
        self.oidc = oidc            
        return {'oidc': oidc}
    
    def fetch(self):
        """
        It fetches the metadata from the url and updates the metadata in the database
        :return: The return value is the result of the updateOidcMetadata method.
        """
        req = requests.get(url=self.url)
        if req.status_code == 200:
            self.metadata = req.json()
            return self.updateOidcMetadata(self.metadata)
        
        raise Exception("Unable to get MetaData")
        
        
        
        
    
        
        