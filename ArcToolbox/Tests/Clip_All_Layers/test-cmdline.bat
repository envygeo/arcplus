@echo. -----------------------------------------------------------------
python Scripts\clip_all_layers.py "Clip All Layers test.mxd" scratch\source.gdb\clip_poly scratch\clipped.gdb

@echo off
echo.
echo.
echo. -----------------------------------------------------------------
echo. Expected:
echo.    "Clip Results\waterbody"         skipping broken layer
echo.    "Clip Results\clip_poly"         skipping broken layer
echo.    "Clip Results\random_rast"       skipping broken layer
echo.    "Source\clip_poly"       Clipping...
echo.    "Source\waterbody"       Clipping...
echo.    "Source\random_rast"     Clipping...
echo.    Executing: Clip GPL0 # scratch\clipped.gdb\random_rast scratch\source.gdb\clip_poly # ClippingGeometry NO_MAINT
echo.    AIN_EXTENT
echo.    Start Time: Thu Feb 26 10:27:13 2015
echo.    Succeeded at Thu Feb 26 10:27:17 2015 (Elapsed Time: 3.18 seconds)
echo. -----------------------------------------------------------------
