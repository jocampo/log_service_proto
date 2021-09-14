import fnmatch
import os
import pathlib
import shutil
import subprocess
import re

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
          f"--python_out={proto_dir} " \
          f"--grpc_python_out={proto_dir} " \
          f"{' '.join(proto_files)}"

subprocess.run(command, shell=True)

# Our output parent folder need to have an __init__.py file
init = open(join(proto_dir, '__init__.py'), 'w+')
init.close()

# Matches imports that start with from ____ import **** (that need to get fixed)
module_import_pattern = re.compile("(?m)^(from[ ]+(\S+)[ ]+)import[ ]+(\S+)[ ]*")

# Matches the from ___ import strings, we care about group 1 (the module name of the import)
module_import_name_pattern = "from[ ](.*?)[ ]import"
parent_module_name = "log_service_proto"

for directory in proto_out_dirs:
    # Our output subfolders need to have an __init__.py file
    init_path = join(proto_dir, directory)
    init_py = open(join(init_path, '__init__.py'), 'w+')
    init_py.close()

    for root, dirname, filenames in os.walk(join(proto_dir, directory)):
        for filename in [f for f in filenames if "pb" in f and ".py" in f]:
            # Read python file into memory (safest this way)
            with open(join(root, filename), "r") as py_file:
                lines = py_file.readlines()

            # Check line by line if they contain broken module imports
            for num, line in enumerate(lines):
                if module_import_pattern.match(line):
                    module_name = re.search(module_import_name_pattern, line).group(1)
                    if module_name in proto_out_dirs:
                        new_module_name = f"{parent_module_name}.{module_name}"

                        # Perform the replacement (mutating the original lines)
                        new_line = line.replace(module_name, new_module_name, 1)
                        lines[num] = new_line

            # Write the new lines into the file (overwriting it)
            with open(join(root, filename), "w") as py_file:
                py_file.writelines(lines)


