#!/usr/bin/python

import fnmatch
import os
import pathlib
import shutil
import subprocess
from os.path import abspath, isfile, join

PWD = pathlib.Path(__file__).parent.resolve()

proto_path = abspath(join(PWD, "..", "proto", "src"))
proto_dir = join(PWD, "proto_out")

js_file = join(PWD, "proto-objects.js")
if os.path.exists(js_file):
    os.remove(js_file)

ts_file = join(PWD, "proto-objects.d.ts")
if os.path.exists(ts_file):
    os.remove(ts_file)

if os.path.exists(proto_dir):
    shutil.rmtree(proto_dir)

shutil.copytree(proto_path, proto_dir)

proto_files = []
for root, dirnames, filenames in os.walk(proto_path):
    for filename in fnmatch.filter(filenames, '*.proto'):
        proto_files.append(filename)  # can also use root for abs path

print(proto_files)

# JavaScript
subprocess.run(["pbjs", "--path", proto_dir, " ".join(proto_files)])
# pbjs --path "${PROTO_DIR}" ${TOP_LEVEL_PROTOS[@]}
