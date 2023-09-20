import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

# Constants
INDEX = 1.53  # Refractive index
FOCAL_LENGTH = 40  # [mm]
DIAMETER = 25.4  # [mm]
NUM_SEGMENTS = 4  # Lens segmentations
RADIUS_OF_CURVATURE = FOCAL_LENGTH * (INDEX - 1)
THICKNESS = 0.5  # [mm]
LDA = 0.299792  # [mm], (1 THz)


def compute_lens_profile():
    radius = np.linspace(0, DIAMETER / 2 + 0.1, 1000)
    y = radius**2 / (2 * RADIUS_OF_CURVATURE)
    y = y[-1] - y
    d = LDA / INDEX
    y = y[::-1]
    indices = np.arange(0, len(y), ceil(len(y) / NUM_SEGMENTS))

    for i in indices:
        y[i:] -= d * (y[i] // d)
    y = y[::-1]
    y += THICKNESS
    return radius, y, indices


def plot_lens_profile(radius, y, diameter):
    fig, ax = plt.subplots(figsize=(diameter, y.max()))
    ax.fill_between(
        np.concatenate([-radius[::-1], radius]), np.concatenate([y[::-1], y]), alpha=0.2
    )
    for pos in ["top", "right", "left", "bottom"]:
        ax.spines[pos].set_visible(False)
    ax.set(xticks=[], yticks=[], xticklabels=[], yticklabels=[])
    fig.savefig("lens.png", dpi=320)
    plt.show()


def save_lens_profile(radius, y, indices):
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    indices = np.concatenate((indices, [len(y) - 1]))
    slices = [slice(indices[i], indices[i + 1] - 2) for i in range(len(indices) - 1)]
    connecting_points = [
        (radius[indices[i + 1]], y[indices[i + 1]]) for i in range(len(indices) - 1)
    ]
    spline_coords = [[(x, y) for x, y in zip(radius[s], y[s])] for s in slices]

    for i in range(len(spline_coords)):
        msp.add_spline(spline_coords[i])
        msp.add_line(spline_coords[i][-1], connecting_points[i])

    msp.add_line(connecting_points[-1], (radius[-1], 0))
    msp.add_line((radius[-1], 0), (0, 0))
    msp.add_line((0, 0), (0, y[0]))

    # Set document units to mm
    doc.header["$INSUNITS"] = 4

    # Save the DXF document to a file
    doc.saveas("lens_profile.dxf")


if __name__ == "__main__":
    radius, y, indices = compute_lens_profile()
    plot_lens_profile(radius, y, DIAMETER)
    save_lens_profile(radius, y, indices)
