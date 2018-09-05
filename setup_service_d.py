#! /usr/bin/python
# -*- coding: utf-8 -*-


from distutils.core import setup
import py2exe


from glob import glob
               
zipfile_path = "lib\shardlib.dll"

               
setup(
    options = {"py2exe": {"optimize": 2,
                            "compressed": 1,
                            "dll_excludes": ["MSVCP90.dll",],
                            "bundle_files": 1,
                            "includes": ["sip"]},
                
    },
    name = "pypod_service_d",
    version = "1.0.0",
    description = "pypod_service_d",
    zipfile = None,
    service=[
              {   
                'modules': 'pypod_service_d',
                "uac_info":"highestAvailable",
              }
             ]
)

