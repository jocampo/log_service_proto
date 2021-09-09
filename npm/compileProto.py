#!/usr/bin/python

import fnmatch
import os
import pathlib
import shutil
import subprocess
from os.path import abspath, isfile, join

PWD = pathlib.Path(__file__).parent.resolve()

# Proto output file names
JS_FILE_NAME = "log-service-proto.js"
TS_FILE_NAME = "log-service-proto.d.ts"

# The folder where the protobuf files live:
proto_path = abspath(join(PWD, "..", "proto", "src"))

# Output folder (where the js/ts definitions will be generated)
proto_dir = join(PWD, "proto_out")

js_file = join(proto_dir, JS_FILE_NAME)
if os.path.exists(js_file):
    os.remove(js_file)

ts_file = join(proto_dir, TS_FILE_NAME)
if os.path.exists(ts_file):
    os.remove(ts_file)

if os.path.exists(proto_dir):
    shutil.rmtree(proto_dir)

shutil.copytree(proto_path, proto_dir)

proto_files = []
for root, dirnames, filenames in os.walk(proto_path):
    for filename in fnmatch.filter(filenames, '*.proto'):
        # can also use root for abs path
        proto_files.append(join(root, filename))

# JavaScript Definitions
command = f"pbjs -t static-module " \
          f"--path {proto_dir} {' '.join(proto_files)} " \
          f"--out {js_file} " \
          f"--es6"
""
subprocess.run(["pbjs", "-t", "static-module"], shell=True)

# Typescript Definitions
command = f"pbts " \
          f"{js_file} " \
          f"--out {ts_file}"

subprocess.run(command, shell=True)
