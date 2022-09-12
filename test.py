from pyazuread import Baarerstrategy
import pathlib
import json
import unittest


if __name__ == '__main__':
    config = {}
    with open(f'{pathlib.Path(__file__).parent.resolve()}/config.json') as f:
        config = json.loads(f.read())
    token = """Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjJaUXBKM1VwYmpBWVhZR2FYRUpsOGxWMFRPSSJ9.eyJhdWQiOiJhMDc1ZWIxNC01NWNkLTQ3ZWMtOTNjMS0yZmU1ZGJkNTE1ODgiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vOTFhMDViNmEtNTM1Zi00Y2NiLThlMDItYTAzNTk1YzllZmJmL3YyLjAiLCJpYXQiOjE2NjI5NDI0OTEsIm5iZiI6MTY2Mjk0MjQ5MSwiZXhwIjoxNjYyOTQ3OTE2LCJhaW8iOiJBWVFBZS84VEFBQUF3RUFJaU0xNSsxVFBxMjVHOFBRam1ObWp5aDJkS2VGa0kzUUh4bTMxV1NNOUlwdFpuVW5QWjJtOS9jUVdGaytUV2VTV0lqS2E3M1VvZ2FtTjhyRWJJTnhvaHdZOEtoLy80eTZ4TTFiUHl4VDZ4SHZQRDBzaXVwSytrY0dmK29PT21IU012dXpBTFhBcTF6eElKdUJONDcrRHgwcVJSTlJXUGIvenVOVWFWaUk9IiwiYXpwIjoiODhmNGRiYWMtZTk2Ni00ZDcxLWI5MTctM2FhNjU1Zjc3ZWYxIiwiYXpwYWNyIjoiMCIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzQwNjA1YTU3LWQ5NTctNGE5ZC1hMGFkLWJkZmY2NjIzZjVkYy8iLCJuYW1lIjoiU3VtYW4gRGV5Iiwib2lkIjoiMzk1YjRhNzYtNzc1Ny00OTJhLWI5YmMtMTdmMjkyNzFhYzQyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2RleUBzdXJ2ZXltb25rZXkuY29tIiwicmgiOiIwLkFYMEFhbHVna1Y5VHkweU9BcUExbGNudnZ4VHJkYUROVmV4SGs4RXY1ZHZWRllpY0FMSS4iLCJzY3AiOiJhY2Nlc3NfYXNfdXNlciIsInN1YiI6InNYV1RIdjlyVzhGS2std2JzN2VGUmd4UUJiSTJCTmRFckFqUDVQdjJEN28iLCJ0aWQiOiI5MWEwNWI2YS01MzVmLTRjY2ItOGUwMi1hMDM1OTVjOWVmYmYiLCJ1dGkiOiJRd1U5a1I0Sk8wR090YXAxbXdBdkFBIiwidmVyIjoiMi4wIn0.lx1BG96fDfxREZWzrYc3ZWoyxPNlZ1ChcWRfqMYXkE9lsi7G2fhV78In5eUUsHK8dUSMem3Kc9Odx4cH4IO2PNDgii5zsxTo7FCp_-uhqxuP5Vnt_LAgE2moVDpvc-utFSC1BQnBwpMZXPszsFgNmpyHnB7IgvjCYXS3sPq0RpyDQLmKUE3whZikrOW-Bt1lEWj9yQlmrR9wtTSvbhBQNwjb32Y61E2d5CiVkPWDukD1HC3D-Nxz9mDWvUiQmrmioB2OGpnd_PLmoSTvWnhNHUVZpWlthUTmMW6P8NVrMh-W6FpbRTuJnVxx4bHiEUq-1fQJYmqOIwjGRoAoWAWqMA"""    
    options = {
        'identityMetadata': f"https://{config['metadata']['authority']}/{config['credentials']['tenantID']}/{config['metadata']['version']}/{config['metadata']['discovery']}",
        'issuer': f"https://{config['metadata']['authority']}/{config['credentials']['tenantID']}/{config['metadata']['version']}",
        'clientID': config['credentials']['clientID'],
        'audience': config['credentials']['audience'],
        'validateIssuer': config['settings']['validateIssuer'],
        'passReqToCallback': config['settings']['passReqToCallback'],
        'loggingLevel': config['settings']['loggingLevel'],
        'scope': config['resource']['scope'],
        'tenentId': config['credentials']['tenantID']
    }
    try:        
        strategy = Baarerstrategy(options, token).verify()
        print(strategy)
    except Exception as e:
        print(str(e))
    