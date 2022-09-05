echo ':: Building distributions (wheel and src dist)'
python3 -m build >/dev/null

echo ':: Cleaning up'
rm -rf Explicatio.egg-info >/dev/null
rm -rf explicatio/__pycache__ >/dev/null