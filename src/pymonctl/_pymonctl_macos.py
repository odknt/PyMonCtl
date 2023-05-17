#!/usr/bin/python
# -*- coding: utf-8 -*-
# Incomplete type stubs for pyobjc
# mypy: disable_error_code = no-any-return
from __future__ import annotations

import sys

assert sys.platform == "darwin"

from typing import Optional, List

import AppKit
import Quartz

from pymonctl import Structs, pointInBox


def __getAllMonitors(name: str = ""):
    screens = AppKit.NSScreen.screens()
    for screen in screens:
        desc = screen.deviceDescription()
        displayId = desc['NSScreenNumber']  # Quartz.NSScreenNumber seems to be wrong
        try:
            scrName = screen.localizedName() + "_" + str(displayId)  # In older macOS, screen doesn't have localizedName() method
        except:
            scrName = "Display" + "_" + str(displayId)

        if not name or (name and scrName == name):
            yield [screen, desc, displayId, scrName]
            if name:
                break


def __getDisplayId(name: str = ""):
    displayId = 0
    if name:
        for mon in __getAllMonitors(name):
            screen, desc, displayId, scrName = mon
            displayId = desc['NSScreenNumber']
            break
    else:
        displayId = Quartz.CGMainDisplayID()
    return displayId


def _getAllScreens():
    result: dict[str, Structs.ScreenValue] = {}
    for mon in __getAllMonitors():
        screen, desc, displayId, scrName = mon

        display = displayId
        is_primary = Quartz.CGDisplayIsMain(display) == 1
        x, y, w, h = int(screen.frame().origin.x), int(screen.frame().origin.y), int(screen.frame().size.width), int(screen.frame().size.height)
        wa = screen.visibleFrame()
        wx, wy, wr, wb = int(wa.origin.x), int(wa.origin.y), int(wa.size.width), int(wa.size.height)
        scale = int(screen.backingScaleFactor() * 100)
        dpi = desc[Quartz.NSDeviceResolution].sizeValue()
        dpiX, dpiY = int(dpi.width), int(dpi.height)
        rot = int(Quartz.CGDisplayRotation(display))
        freq = Quartz.CGDisplayModeGetRefreshRate(Quartz.CGDisplayCopyDisplayMode(display))
        depth = Quartz.CGDisplayBitsPerPixel(display)

        result[scrName + "_" + str(display)] = {
            'id': display,
            'is_primary': is_primary,
            'pos': Structs.Point(x, y),
            'size': Structs.Size(w, h),
            'workarea': Structs.Rect(wx, wy, wr, wb),
            'scale': (scale, scale),
            'dpi': (dpiX, dpiY),
            'orientation': rot,
            'frequency': freq,
            'colordepth': depth
        }
    return result


def _getMonitorsCount() -> int:
    return len(AppKit.NSScreen.screens())


def _getScreenSize(name: str = "") -> Optional[Structs.Size]:
    res: Optional[Structs.Size] = None
    if name:
        for mon in __getAllMonitors(name):
            screen, desc, displayId, scrName = mon
            size = screen.frame().size
            res = Structs.Size(int(size.width), int(size.height))
            break
    else:
        size = AppKit.NSScreen.mainScreen().frame().size
        res = Structs.Size(int(size.width), int(size.height))
    return res


def _getWorkArea(name: str = "") -> Optional[Structs.Rect]:
    res: Optional[Structs.Rect] = None
    if name:
        for mon in __getAllMonitors(name):
            screen, desc, displayId, scrName = mon
            wa = screen.visibleFrame()
            wx, wy, wr, wb = int(wa.origin.x), int(wa.origin.y), int(wa.size.width), int(wa.size.height)
            res = Structs.Rect(wx, wy, wr, wb)
            break
    else:
        wa = AppKit.NSScreen.mainScreen().visibleFrame()
        wx, wy, wr, wb = int(wa.origin.x), int(wa.origin.y), int(wa.size.width), int(wa.size.height)
        res = Structs.Rect(wx, wy, wr, wb)
    return res


def _getPosition(name: str = "") -> Optional[Structs.Point]:
    res: Optional[Structs.Point] = None
    if name:
        for mon in __getAllMonitors(name):
            screen, desc, displayId, scrName = mon
            origin = screen.frame().origin
            res = Structs.Point(int(origin.x), int(origin.y))
            break
    else:
        origin = AppKit.NSScreen.mainScreen().frame().origin
        res = Structs.Point(int(origin.x), int(origin.y))
    return res


def _getRect(name: str = "") -> Optional[Structs.Rect]:
    res: Optional[Structs.Rect] = None
    if name:
        for mon in __getAllMonitors(name):
            screen, desc, displayId, scrName = mon
            frame = screen.frame()
            res = Structs.Rect(int(frame.origin.x), int(frame.origin.y),
                               int(frame.origin.x) + int(frame.size.width), int(frame.origin.y) + int(frame.size.height))
            break
    else:
        frame = AppKit.NSScreen.mainScreen().frame()
        res = Structs.Rect(int(frame.origin.x), int(frame.origin.y),
                           int(frame.origin.x) + int(frame.size.width),  int(frame.origin.y) + int(frame.size.height))
    return res


def _findMonitorName(x: int, y: int) -> str:
    name = ""
    screens = AppKit.NSScreen.screens()
    for screen in screens:
        frame = screen.frame()
        if pointInBox(x, y, int(frame.origin.x), int(frame.origin.y), int(frame.size.width), int(frame.size.height)):
            desc = screen.deviceDescription()
            displayId = desc['NSScreenNumber']  # Quartz.NSScreenNumber seems to be wrong
            try:
                name = screen.localizedName() + "_" + str(displayId)  # In older macOS, screen doesn't have localizedName() method
            except:
                name = "Display" + "_" + str(displayId)
    return name


def _getCurrentMode(name: str = "") -> Optional[Structs.DisplayMode]:
    res: Optional[Structs.DisplayMode] = None
    displayId = __getDisplayId(name)
    if displayId:
        mode = Quartz.CGDisplayCopyDisplayMode(displayId)
        w = Quartz.CGDisplayModeGetWidth(mode)
        h = Quartz.CGDisplayModeGetHeight(mode)
        r = Quartz.CGDisplayModeGetRefreshRate(mode)
        res = Structs.DisplayMode(w, h, r)
    return res


def _getAllowedModes(name: str = "") -> List[Structs.DisplayMode]:
    modes: List[Structs.DisplayMode] = []
    displayId = __getDisplayId(name)
    if displayId:
        allModes = Quartz.CGDisplayCopyAllDisplayModes(displayId, None)
        for mode in allModes:
            w = Quartz.CGDisplayModeGetWidth(mode)
            h = Quartz.CGDisplayModeGetHeight(mode)
            r = Quartz.CGDisplayModeGetRefreshRate(mode)
            modes.append(Structs.DisplayMode(w, h, r))
    return modes


def _changeMode(mode: Structs.DisplayMode, name: str = ""):
    # https://stackoverflow.com/questions/10596489/programmatically-change-resolution-os-x
    displayId = __getDisplayId(name)
    if displayId:
        allModes = Quartz.CGDisplayCopyAllDisplayModes(displayId, None)
        for m in allModes:
            w = Quartz.CGDisplayModeGetWidth(m)
            h = Quartz.CGDisplayModeGetHeight(m)
            r = Quartz.CGDisplayModeGetRefreshRate(m)
            if w == mode.width and h == mode.height and r == mode.frequency:
                Quartz.CGDisplaySetDisplayMode(displayId, m, None)


def _changeScale(scale: int, name: str = ""):
    pass


def _changeOrientation(orientation: int, name: str = ""):
    pass


def _changePosition(newX: int, newY: int, name: str = ""):
    pass


def _getMousePos(unflipValues: bool = False) -> Structs.Point:
    """
    Get the current (x, y) coordinates of the mouse pointer on screen, in pixels

    Notice in AppKit the origin (0, 0) is bottom left (unflipped), which may differ to coordinates obtained
    using AppScript or CoreGraphics (flipped). To manage this, use 'unflipValues' accordingly.

    :param unflipValues: set to ''True'' to convert coordinates to origin (0, 0) at upper left corner
    :return: Point struct
    """
    # https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python/24567802
    mp = Quartz.NSEvent.mouseLocation()
    x, y = int(mp.x), int(mp.y)
    if unflipValues:
        screens = AppKit.NSScreen.screens()
        for screen in screens:
            frame = screen.frame()
            sx, sy, sw, sh = int(frame.origin.x), int(frame.origin.y), int(frame.size.width), int(frame.size.height)
            if pointInBox(x, y, sx, sy, sw, sh):
                y = (-1 if y < 0 else 1) * int(sh) - abs(y)
                break
    return Structs.Point(x, y)
