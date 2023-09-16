# Fresnel lens generator

This project contains two parts:

  1. A script that generates the DXF profile of a Fresnel plano-convex lens, assuming a known refractive index and diameter.
  2. A FreeCAD macro that imports the DXF profile into a Sketch, which can be revolved into an object for 3D printing.

Dependencies
------------
 - FreeCAD:
   - A terrific open-source parametric 3D modelling software.
 - ezdxf
   - A Python package for programmatic definition of DXF files.

![Lens profile](lens.png)
