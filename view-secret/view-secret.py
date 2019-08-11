#!/usr/bin/python

import sys
import os
import subprocess
import json
import base64

def writeStdErr(message):
    sys.stderr.write('{0}\n'.format(message))

if len(sys.argv) < 2: 
    writeStdErr('error: secret name required')
    exit(1)

a = sys.argv

secret = a[1] if len(a) > 1 else None
key = a[2] if len(a) > 2 else None
ns = a[3] if len(a) > 3 else None

extra = []
if ns:
    extra = ['--namespace=%s'%(ns)]

secret_obj = json.loads(subprocess.check_output(['kubectl', 'get', 'secret',  secret,  '-o=json' ] + extra))
data = secret_obj['data']

if not key:
    if len(data) > 1:
        writeStdErr('Multiple sub keys found. Specify another argument, one of:')
        for k in data.keys():
            writeStdErr('-> %s' %(k))
        exit(1)
    elif len(data) == 1: 
        key = data.keys()[0]
        writeStdErr('Choosing key: %s' %(key))
    else:
        writeStdErr('Unexpected situation, no data in secret')
        exit(1)

print(base64.b64decode(data[key]).decode("utf-8"))
