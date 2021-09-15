## Creating a new set of python proto classes
1. Create a venv (py > 3.5 ish)
2. Install dependencies (see `requirements.txt`).
   1. TODO: this file has WAY more dependencies than it should. Clean it up.
3. In this folder (`python/`), run:

```shell
python ./compileProto.py
```

- Output should be in the `log_service_proto/` folder

## Creating a new build
See [this post](https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi) for more notes and examples about the packaging process.

1. Install the required dependencies (they don't need to be in the venv):
    ```shell
    python -m pip install --user --upgrade setuptools wheel build
    python -m pip install --user --upgrade twine
    ```
2. Update the `setup.cfg` file with any changes (such as new version number)
3. Generate the build
    ```shell
    python3 -m build
    ```
4. **Make sure** that the files in `dist/` reflect what you want to release. Often times `setup.cfg` has errors in it and that causes issues like files being omitted from the dist folders.

## Publish to Test Pypi repo
1. Upload the dist files to TestPypi
   ```shell
    python3 -m twine upload --repository testpypi dist/*
   ```
   **Note:** In case your files contain old releases. These WILL try to get uploaded again. You can prevent that by adding the flag: 
          `--skip-existing`
    
2. You can install the package (in other projects) with: 
    ```shell
    pip install -i https://test.pypi.org/simple/ jocampo-log-service-proto
    ```

## Publish to the actual Pypi repo 
1. Upload the dist files to Pypi
   ```shell
    python3 -m twine upload dist/*
   ```
   **Note:** In case your files contain old releases. These WILL try to get uploaded again. You can prevent that by adding the flag: 
          `--skip-existing`
    
2. You can install the package (in other projects) with: 
    ```shell
    pip install jocampo-log-service-proto
    ```