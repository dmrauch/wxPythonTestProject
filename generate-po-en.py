#! /usr/bin/env python3
"""
Create English .po file from .pot template

Call with "python generate-po-en.py <potFile>".
"""

import os
import sys

assert len(sys.argv) == 2, "Usage: python generate-po-en.py <potFile>"
potFileName = sys.argv[1]
assert os.path.isfile(potFileName), ".pot file does not exist"
assert os.path.split(potFileName)[1].endswith(".pot"), "file name has to end with '.pot'"

appName = os.path.split(potFileName)[1].replace(".pot", "")
poFilePath = "locale/en/LC_MESSAGES"
poFileName = os.path.join(poFilePath, appName+".po")
if not os.path.isdir(poFilePath):
  os.makedirs(poFilePath)

print("appName:     {}".format(appName))
print("potFileName: {}".format(potFileName))
print("poFileName:  {}".format(poFileName))
print("")

with open(potFileName, "rt", buffering = 1) as pot:
  with open(poFileName, "wt") as po:

    for potLine in pot:

      if potLine.startswith("msgid"):
        msgid = potLine
        msgstr = pot.readline()
        assert msgstr.startswith("msgstr"), "something is wrong with the pot file"
        po.write(msgid)
        po.write(msgid.replace("msgid", "msgstr"))

      elif potLine.startswith("\"Content-Type:"):
        po.write(potLine.replace("CHARSET", "UTF-8"))

      else:
        po.write(potLine)

print("Successfully wrote pot file")
