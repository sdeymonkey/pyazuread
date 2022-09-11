from pyazuread import Baarerstrategy
import pathlib
import json
import unittest


if __name__ == '__main__':
    config = {}
    with open(f'{pathlib.Path(__file__).parent.resolve()}/config.json') as f:
        config = json.loads(f.read())
    token = """Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.MrP-Q2zJHHTyEylpM3O3y_2XFPUgR0OWfzO7ZwjDJq8"""    
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
    