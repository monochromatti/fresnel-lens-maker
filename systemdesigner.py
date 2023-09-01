import numpy as np
import matplotlib.pyplot as plt


class Ray:
    def __init__(self, origin, angle):
        self.origin = np.array(origin)
        self.angle = angle
        self.path = [origin]

    def propagate(self, distance):
        """Move the ray forward by the given distance"""
        dx = distance * np.cos(self.angle)
        dy = distance * np.sin(self.angle)
        new_point = self.origin + np.array([dx, dy])
        self.path.append(new_point)
        self.origin = new_point


class Lens:
    def __init__(self, position, focal_length):
        self.position = position
        self.focal_length = focal_length

    def interact(self, ray):
        """Update the ray's direction based on the lens's properties"""
        u = self.position - ray.origin[0]
        if self.focal_length == np.inf:  # Handle the case of a plane mirror
            v = np.inf
        else:
            v = 1 / (1 / self.focal_length + 1 / u)
        ray.angle = np.arctan((ray.origin[1] + u * np.tan(ray.angle)) / v)


class LightSource:
    def __init__(self, position, size, divergence_angle):
        self.position = position
        self.size = size
        self.divergence_angle = divergence_angle

    def generate_rays(self, n_rays=10):
        """Generate rays from the light source"""
        rays = []
        for i in np.linspace(-self.size / 2, self.size / 2, n_rays):
            for angle in np.linspace(
                -self.divergence_angle / 2, self.divergence_angle / 2, n_rays
            ):
                rays.append(Ray([self.position, i], angle))
        return rays


class OpticalSystem:
    def __init__(self):
        self.lenses = []
        self.light_source = None
        self.rays = []

    def add_lens(self, lens):
        self.lenses.append(lens)

    def set_light_source(self, light_source):
        self.light_source = light_source

    def trace_rays(self, distance):
        """Trace the rays through the optical system"""
        if not self.light_source:
            raise ValueError("No light source set!")
        self.rays = self.light_source.generate_rays()
        for ray in self.rays:
            for lens in sorted(self.lenses, key=lambda x: x.position):
                while ray.origin[0] < lens.position:
                    ray.propagate(0.1)
                lens.interact(ray)
            ray.propagate(distance - ray.origin[0])

    def plot(self):
        """Plot the optical system and the rays"""
        fig, ax = plt.subplots(figsize=(10, 6))
        for ray in self.rays:
            path = np.array(ray.path)
            ax.plot(path[:, 0], path[:, 1], color="blue")
        for lens in self.lenses:
            ax.axvline(lens.position, color="k", linestyle="--")
        ax.set_title("Optical System Ray Tracing")
        ax.set_xlabel("Position (x)")
        ax.set_ylabel("Position (y)")
        ax.grid(True)
        plt.show()


class GaussianBeamSource:
    def __init__(self, position, w0, wavelength, n_rays=10):
        self.position = position
        self.w0 = w0  # Beam waist size
        self.wavelength = wavelength
        self.zR = np.pi * w0**2 / wavelength  # Rayleigh range
        self.theta = wavelength / (np.pi * w0)  # Beam divergence
        self.n_rays = n_rays

    def beam_radius(self, z):
        """Calculate the beam radius at position z"""
        return self.w0 * np.sqrt(1 + ((z - self.position) / self.zR) ** 2)

    def generate_rays(self):
        """Generate rays based on the Gaussian beam parameters"""
        rays = []
        # Calculate the beam size at the source position
        beam_size = self.beam_radius(self.position)
        for i in np.linspace(-beam_size, beam_size, self.n_rays):
            angle = np.arctan(i * self.theta / beam_size)
            rays.append(Ray([self.position, i], angle))
        return rays


def waist_from_divergence(theta, wavelength):
    """Calculate the beam waist from the divergence angle"""
    return 



if __name__ == "__main__":
    theta = np.deg2rad(4)
    wavelength = 0.599

    w0 = wavelength / (np.pi * theta) # Waist size in mm
    zR = np.pi * w0**2 / wavelength

    # Set up the optical system with the new parameters
    source = GaussianBeamSource(0, w0, wavelength, n_rays=10)

    lens = Lens(30, 0.3)
    # lens2 = Lens(40, 70)

    system = OpticalSystem()
    system.add_lens(lens)
    system.set_light_source(source)
    system.trace_rays(200)
    system.plot()