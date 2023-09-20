# Fresnel-lens maker

![Lens profile](lens.png)

This project contains two parts:

  1. A script that generates the DXF profile of a Fresnel plano-convex lens, assuming a known refractive index and diameter.
  2. A FreeCAD macro that imports the DXF profile into a Sketch object, which can be revolved into an object for 3D printing.

By setting the thickness of the segments such that phase delay across the lens is equal everywhere modulo 2π, no phase distortions are induced at the design wavelength.

Dependencies
------------
 - FreeCAD:
   - A terrific open-source parametric 3D modelling software.
 - ezdxf
   - A Python package for programmatic definition of DXF files.

Instructions
------------
  1. Set the global variables in lens_maker.py to your specifications (lens diameter, focal length, refractive index, and number of segments).
  2. Running it (`python lens_maker.py`) produces a PNG (for inspection) and a DXF (for next step).
  3. In FreeCAD, load the macro SketchDXF and run it (it prompts you to select the DXF).
     1. Enter the *Part Design workbench*.
     2. Select the macro-generated Sketch, and run *Revolution*.
     3. Export the `Body` (or a `Mesh`) into your desired 3D printing format.
