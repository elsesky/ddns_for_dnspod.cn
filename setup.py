#! /usr/bin/python
# -*- coding: utf-8 -*-


from distutils.core import setup
import py2exe


from glob import glob
 
data_files = [
                ('', ['./site.ini']),
                ('', ['./user.tpl.ini']),
              ]
               
               
zipfile_path = "lib\shardlib.dll"

               
setup(
    options = {"py2exe": {"optimize": 2,
                            "compressed": 1,
                            "dll_excludes": ["MSVCP90.dll",],
                            "bundle_files": 1,
                            "includes": ["sip"]},
                
    },
    name = "dnspod_ddns_cmd",
    version = "1.0.0",
    description = "dnspod_ddns_cmd_tools",
    zipfile = None,
    console=[
              {   'script': 'pypod.py',
                  "uac_info":"highestAvailable",
              }
             ],
    data_files = data_files
)

