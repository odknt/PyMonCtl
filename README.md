# PyMonCtl
[![Type Checking](https://github.com/Kalmat/PyMonCtl/actions/workflows/type-checking.yml/badge.svg)](https://github.com/Kalmat/PyMonCtl/actions/workflows/type-checking.yml)
[![PyPI version](https://badge.fury.io/py/PyMonCtl.svg)](https://badge.fury.io/py/PyMonCtl)


Cross-Platform module which provides a set of features to get info on and control monitors.

| Monitor features: |
|:-----------------:|
|    getMonitors    |
| getMonitorsCount  |
|      getSize      |
|    getWorkArea    |
|    getPosition    |
|      getRect      |
|  findMonitorInfo  |
|  findMonitorName  |
|    getMousePos    |
|  getCurrentMode   |
|  getAllowedModes  |
|    changeMode     |

## Keep Monitors info updated

These features include a watchdog, running in a separate Thread, which will allow you to keep monitors 
information updated and define hooks and its callbacks to be notified when monitors are plugged/unplugged or 
their properties change. 

| watchdog methods:  |
|:------------------:|
|    enableUpdate    |
|   disableUpdate    |
|  isUpdateEnabled   |
|   updateInterval   |

Notice this is a module-level information, completely independent (though related to and used by) window objects.
Also notice that the information provided by `getMonitors()` method will be static unless the watchdog is enabled,
or invoked with `forceUpdate=True`.

Enable this only if you need to keep track of monitor-related events like changing its resolution, position,
or if monitors can be dynamically plugged or unplugged in a multi-monitor setup. If you need monitors info updated 
at a given moment, but not continuously updated, just invoke getMonitors(True/False) at your convenience.

If enabled, it will activate a separate thread which will periodically update the list of monitors and
their properties (see getMonitors() function).

If disabled, the information on the monitors connected to the system will be static as it was when
PyMonCtl module was initially loaded (changes produced afterwards will not be returned by `getMonitors()`).

By default, the monitors info will be checked (and updated) every 0.3 seconds. Adjust this value to your needs, 
but take into account higher values will take longer to detect and notify changes; whilst lower values will 
consume more CPU.

## Get notifications on Monitors changes

When enabling the watchdog using `enableUpdate()`, it is possible to define callbacks to be invoked in case the 
number of connected monitors or their properties change. The information passed to the callbacks is:

   - Names of the monitors which have changed (as a list of strings)
   - All monitors info, as returned by getMonitors()

To access monitors properties, use monitor name as dictionary key

    monitorCountChange: callback to invoke when a monitor is plugged or unplugged
                        Passes the list of monitors that produced the event and the info on all monitors (see getMonitors())
    
    monitorPropsChange: callback to invoke if a monitor changes its properties (e.g. position or resolution)
                        Passes the list of monitors that produced the event and the info on all monitors (see getMonitors())

Example:

    import pymonctl as pmc
    import time

    def countChanged(names, screensInfo):
        print("MONITOR PLUGGED/UNPLUGGED:", names)
        for name in names:
            print("MONITORS INFO:", screensInfo[name])

    def propsChanged(names, screensInfo):
        print("MONITOR CHANGED:", names)
        for name in names:
            print("MONITORS INFO:", screensInfo[name])

    pmc.enableUpdate(monitorCountChanged=countChanged, monitorPropsChanged=propsChanged)
    print("Plug/Unplug monitors, or change monitor properties while running")
    print("Press Ctl-C to Quit")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    pmc.disableUpdate()


## INSTALL <a name="install"></a>

To install this module on your system, you can use pip: 

    pip install pymonctl

or

    python3 -m pip install pymonctl

Alternatively, you can download the wheel file (.whl) available in the [Download page](https://pypi.org/project/PyMonCtl/#files) and the [dist folder](https://github.com/Kalmat/PyMonCtl/tree/master/dist), and run this (don't forget to replace 'x.x.xx' with proper version number):

    pip install PyMonCtl-x.x.xx-py3-none-any.whl

You may want to add `--force-reinstall` option to be sure you are installing the right dependencies version.

Then, you can use it on your own projects just importing it:

    import pymonctl

## SUPPORT <a name="support"></a>

In case you have a problem, comments or suggestions, do not hesitate to [open issues](https://github.com/Kalmat/PyMonCtl/issues) on the [project homepage](https://github.com/Kalmat/PyMonCtl)

## USING THIS CODE <a name="using"></a>

If you want to use this code or contribute, you can either:

* Create a fork of the [repository](https://github.com/Kalmat/PyMonCtl), or 
* [Download the repository](https://github.com/Kalmat/PyMonCtl/archive/refs/heads/master.zip), uncompress, and open it on your IDE of choice (e.g. PyCharm)

Be sure you install all dependencies described on `docs/requirements.txt` by using pip
    
    python3 -m pip install -r requirements.txt

## TEST <a name="test"></a>

To test this module on your own system, cd to `tests` folder and run:

    python3 test_pymonctl.py