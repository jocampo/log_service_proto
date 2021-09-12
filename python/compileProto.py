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
proto_dir = join(PWD, "log_service_proto")

if os.path.exists(proto_dir):
    shutil.rmtree(proto_dir)

shutil.copytree(proto_path, proto_dir)

proto_files = []
proto_out_dirs = set()
for root, dirname, filenames in os.walk(proto_path):
    if len(dirname):
        # We'll need these later
        proto_out_dirs.update(dirname)
    for filename in fnmatch.filter(filenames, '*.proto'):
        proto_files.append(join(root, filename))

command = f"python -m grpc_tools.protoc " \
          f"-I {proto_path} " \
          f"--python_out={proto_dir} "  \
          f"--grpc_python_out={proto_dir} " \
          f"{' '.join(proto_files)}"

subprocess.run(command, shell=True)

init = open(join(proto_dir, '__init__.py'), 'w+')
init.close()

# Our output folders need to have an __init__.py file
for directory in proto_out_dirs:
    init_path = join(proto_dir, directory)
    init_py = open(join(init_path, '__init__.py'), 'w+')
    init_py.close()
