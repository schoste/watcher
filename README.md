# watcher
Python script to observe a directoy and execute a command if files changing. You can use it for recompile code or do something else. Previously started commands get killed.

## usage example for auto execute robotframework tests
`watcher.py -d . -e ".*__pycach.*|.*results.*" robot -d results tests/my-tests.robot`

## Required Packages
`pip install watchdog`

`pip install subprocess`

