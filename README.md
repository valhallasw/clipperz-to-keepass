clipperz-to-keepass
===================

Converts Clipperz' json format to Keepass v2 XML.

Usage
-----
### Exporting JSON from Clipperz

1. Log in to https://clipperz.is/
2. Go to 'data' (top menu bar)
3. Go to 'export' (left menu bar)
4. Click 'export to JSON'
5. Wait
6. Save the exported JSON to a text file (utf-8 encoded)

### Converting JSON to XML
```bash
git clone https://github.com/valhallasw/clipperz-to-keepass
cd clipperz-to-keepass
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python converter.py THE_JSON_FILE THE_XML_FILE
```

### Importing in Keepass v2
1. File » Import...
2. Select KeePass XML (2.x)
3. Select the file under 'Files to be imported'
4. Click 'OK'
5. Select 'Create new IDs'
6. Click 'OK'
7. Remove the '(empty group, please remove)' group
8. Your imported passwords are in 'clipperz.is imported passwords'

Conversion
----------
**Not everything is converted**

Having said that, most important things *are* converted.
* Every *card* is mapped to a single *entry* in Keepass.
* All *fields* are imported;
  * Except for empty fields;
  * The field `web address` is mapped to `URL`;
  * The field `Username or email` is mapped to `UserName`;
  * All other fields are left as-is and are imported as *string field*. Those
    are visible in the detail window an by double clicking the
    entry, under the *Advanced* tab.
  * Duplicate names are solved by adding (1), (2), etc. to the name.
* *Direct logins* are imported as if their URL was a `web address` field.


License
-------
This project is MIT licensed; pull requests are very welcome.
