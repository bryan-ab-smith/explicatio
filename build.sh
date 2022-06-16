python3 setup.py bdist_wheel
rm -rf build/
mv dist/*.whl .
rm -rf dist/
rm -rf explicatio.egg-info
