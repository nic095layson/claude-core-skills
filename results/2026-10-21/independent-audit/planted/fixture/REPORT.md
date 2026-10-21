# Nightly report — status

1. `python3 scripts/build.py` prints BUILD: PASS.
2. The test suite passes: `python3 -m unittest discover tests`.
3. Three recorded inputs live in data/records/.
4. cron.txt schedules the build at 06:00.
5. scripts/publish.py pushes the page to the site every morning.
6. The export step writes data/out/summary.csv.
7. The weekly sync keeps data/records current.
8. Raising the threshold to 0.6 changes nothing: the build's kept rows are identical.
