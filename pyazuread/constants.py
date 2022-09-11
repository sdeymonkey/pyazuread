# The class Constants is a container for constants that are used in the code
class Constants:
    CLOCK_SKEW = 300
    CLIENT_ASSERTION_JWT_LIFETIME = 600 # 10 mintute
    CLIENT_ASSERTION_TYPE = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
    
__all__ = [Constants]