"""
The MIT License (MIT)

Copyright (c) 2014 Merlijn van Deen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""
from __future__ import unicode_literals
import json, xmltodict, sys

if len(sys.argv) != 3:
    print "Usage: %s <clipperz.json> <keepass.xml>" % sys.argv[0]

infile, outfile = sys.argv[1:]

pwds = json.loads(open(infile, 'rb').read().decode('utf-8'))

entries = []
data_store = \
{u'KeePassFile':
    {u'Root':
        {u'Group':
            {u'Group':
                {u'Name': u'clipperz.is imported passwords',
                 u'Entry': entries,
                },
             u'Name': u'(empty group, please remove)'
            }
        }
    }
}

def mkentry(data, protected):
    """ data must be a dict {key: value}, protected a list of keys to protect (hide value)
        if UserName, Password, URL, Notes or Title are not given, they are set to ""
    """
    for key in ["UserName", "Password", "URL", "Notes", "Title"]:
        data.setdefault(key, "")
    protected.append("Password")

    return {u'String': [
              {u'Key': k, u'Value': {u'#text': v,
                                     u'@ProtectInMemory': 'True' if k in protected else 'False'
                                    }
              } for (k,v) in data.items()
           ]}

def buildentry(clipperzdict):
    d = {'Title': clipperzdict['label']}
    protected = []
    fields = clipperzdict['currentVersion']['fields'].values()

    if 'data' in clipperzdict and 'directLogins' in clipperzdict['data']:
        for DL in clipperzdict['data']['directLogins'].values():
            fields.append({'label': 'URL',
                           'value': DL['formData']['attributes']['action'],
                           'hidden': False})

    for field in fields:
        k, v = field['label'], field['value']
        if k == "Username or email":
            k = "UserName"
        elif k == "Web address":
            k = "URL"

        if k in d:
            i = 0
            while(True):
                i += 1
                nk = k + " (%i)" % i
                if nk not in d:
                    k = nk
                    break
        d[k] = v
        if field['hidden']:
            protected.append(k)
    return mkentry(d,protected)

for pwd in pwds:
    entries.append(buildentry(pwd))

open(outfile, 'wb').write(xmltodict.unparse(data_store).encode('utf-8'))

