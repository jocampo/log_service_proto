import fnmatch
import os
import pathlib
import shutil
import subprocess

from os.path import abspath, join

PWD = pathlib.Path(__file__).parent.resolve()

# The folder where the protobuf files live:
proto_path = abspath(join(PWD, "..", "proto", "src"))

# Output folder (where the python definitions will be generated)
proto_dir = join(PWD, "proto_out")

if os.path.exists(proto_dir):
    shutil.rmtree(proto_dir)

shutil.copytree(proto_path, proto_dir)

proto_files = []
for root, _, filenames in os.walk(proto_path):
    for filename in fnmatch.filter(filenames, '*.proto'):
        proto_files.append(join(root, filename))

command = f"python -m grpc_tools.protoc " \
          f"-I {proto_path} " \
          f"--python_out={proto_dir} "  \
          f"--grpc_python_out={proto_dir} " \
          f"{' '.join(proto_files)}"

subprocess.run(command, shell=True)


