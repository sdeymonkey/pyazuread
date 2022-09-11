from requests.models import PreparedRequest
import re


def getLibraryVersionParameterName():
    return "x-client-Ver"

def getLibraryProductParameterName():
    return "x-client-SKU"

def getLibraryProduct():
    return "passport-azure-ad"

def getLibraryVersion():
    return  "4.3.2" 

def concatUrl(base_url, params):
    req = PreparedRequest()
    req.prepare_url(base_url, params)
    return req.url

def isBlank (myString):
    if myString and myString.strip():
        return False
    return True

def is_valid_url(url):
    """
    It checks if the url starts with https://, then checks if the domain is valid, then
    checks if the port is valid, then checks if the path is valid
    
    :param url: The URL to be validated
    :return: A boolean value.
    """
    regex = re.compile(
        r'^https://'  # https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
