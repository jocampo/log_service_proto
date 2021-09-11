import fnmatch
import os
import pathlib
import shutil
import subprocess

from os.path import abspath, join

subprocess.run("pip3 install grpcio-tools", shell=True)

PWD = pathlib.Path(__file__).parent.resolve()

# The folder where the protobuf files live:
proto_path = abspath(join(PWD, "..", "proto", "src"))
proto_root_path = abspath(join(PWD, "..", "proto"))

# Output folder (where the python definitions will be generated)
proto_dir = join(PWD, "proto_out")

if os.path.exists(proto_dir):
    shutil.rmtree(proto_dir)

shutil.copytree(proto_path, proto_dir)

proto_files = []
proto_import_paths = set()
for root, _, filenames in os.walk(proto_path):
    for filename in fnmatch.filter(filenames, '*.proto'):
        # can also use root for abs path
        proto_import_paths.add(root)
        proto_files.append(filename)

proto_import_paths.add(proto_root_path)

command = f"python3 -m grpc_tools.protoc " \
          f"--proto_path {proto_path} --proto_path {' --proto_path '.join(proto_import_paths)} " \
          f"--python_out={proto_dir} " \
          f"--grpc_python_out={proto_dir} " \
          f"{' '.join(proto_files)}"

# python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/helloworld.proto
subprocess.run(command, shell=True)
# python -m grpc_tools.protoc -I . --python_out $PYTHON_OUTPUT_DIR --grpc_python_out $PYTHON_OUTPUT_DIR


