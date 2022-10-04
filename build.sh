# Timing code courtesy of  https://unix.stackexchange.com/a/52347
start=`date +%s.%N`
echo ':: Building distributions (wheel and src dist)'
python3 -m build >/dev/null

echo ':: Cleaning up'
rm -rf Explicatio.egg-info >/dev/null
rm -rf explicatio/__pycache__ >/dev/null
end=`date +%s.%N`

runtime=$( echo "$end - $start" | bc -l )
echo "Build time: $runtime seconds"