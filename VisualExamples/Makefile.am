## Process this file with automake to produce Makefile.in
# Makefile to distribute the example programs

AUTOMAKE_OPTIONS = foreign
srcdir = @srcdir@
VPATH = @srcdir@

if BUILD_EXAMPLES
examplefiles = bounce.py bounce2.py boxlighttest.py colorsliders.py \
	conch.py controlstest.py \
	convex.py crossproduct.py crystal.py differential_gear.py \
	dipole.py doublependulum.py drape.py \
	electric_motor.py extruded_columns.py extrusion_overview.py extrusion_examples.py \
	faces_cone.py faces_heightfield.py flower128.tga gas.py glinfo.py \
	graphtest.py gyro.py gyro2.py hanoi.py labels.py lathe.py \
	lorenz.py mandelbrot.py material_test.py medusa.py \
	orbit.py planar.py randombox.py stars.py \
	stonehenge.py text3D.py texttest.py texture_and_lighting.py \
	texturetest.py tictac.py tictacdat.py \
	toroid_drag.py toroid.py wave.py
else
examplefiles =
endif

pkgdatadir = @visualexampledir@

dist_pkgdata_DATA = $(examplefiles)
