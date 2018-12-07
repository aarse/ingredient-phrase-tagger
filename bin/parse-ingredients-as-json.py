#!/usr/bin/env python
from __future__ import print_function

import sys
import os
import tempfile
import json

from ingredient_phrase_tagger.training import utils

if len(sys.argv) < 2:
    sys.stderr.write('Usage: parse-ingredients-as-json.py FILENAME')
    sys.exit(1)

FILENAME = str(sys.argv[1])
_, tmpFile = tempfile.mkstemp()

with open(FILENAME) as infile, open(tmpFile, 'w') as outfile:
    outfile.write(utils.export_data(infile.readlines()))

tmpFilePath = "../tmp/model_file"
modelFilename = os.path.join(os.path.dirname(__file__), tmpFilePath)
parsed = os.popen("crf_test -v 1 -m %s %s" % (modelFilename, tmpFile)).readlines()
os.system("rm %s" % tmpFile)
print(json.dumps(utils.import_data(parsed), indent=4))
