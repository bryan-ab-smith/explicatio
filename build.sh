#!/bin/bash
echo 'Building wheel'
python3 setup.py bdist_wheel >/dev/null

echo 'Cleaning up build directories'
rm -rf build/ >/dev/null
mv dist/*.whl . >/dev/null
rm -rf dist/ >/dev/null
rm -rf explicatio.egg-info >/dev/null
rm -rf explicatio/__pycache__ >/dev/null