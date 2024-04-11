from mayavi import mlab
import numpy as np

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    end_of_header_index = next(i for i, line in enumerate(lines) if "!END_OF_HEADER" in line.upper())

    data = []
    for line in lines[end_of_header_index + 1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 4:
                x, y, z, intensity = map(float, parts[:4])
                data.append((x, y, z, intensity))
    
    return data

def lattice_transform(a, b, c, alpha, beta, gamma):
    """Compute the lattice transformation matrix."""
    alpha, beta, gamma = np.radians([alpha, beta, gamma])  # Convert to radians
    cos_alpha, cos_beta, cos_gamma = np.cos(alpha), np.cos(beta), np.cos(gamma)
    sin_gamma = np.sin(gamma)
    volume = 1 - cos_alpha**2 - cos_beta**2 - cos_gamma**2 + 2 * cos_alpha * cos_beta * cos_gamma
    volume = np.sqrt(volume)

    # Transformation matrix
    matrix = np.zeros((3, 3))
    matrix[0, 0] = a
    matrix[1, 0] = b * cos_gamma
    matrix[1, 1] = b * sin_gamma
    matrix[2, 0] = c * cos_beta
    matrix[2, 1] = c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma
    matrix[2, 2] = c * volume / sin_gamma

    return matrix

def transform_points(data, matrix):
    """Apply the lattice transformation matrix to the data points."""
    transformed_data = []
    for x, y, z, intensity in data:
        new_point = np.dot(matrix, np.array([x, y, z]))
        transformed_data.append((*new_point, intensity))
    return transformed_data

def plot_data(data):
    xs, ys, zs, intensities = zip(*data)

    # Normalize intensities for color mapping
    min_intensity, max_intensity = min(intensities), max(intensities)
    normalized_intensities = (np.array(intensities) - min_intensity) / (max_intensity - min_intensity)

    fig = mlab.figure(size=(800, 700))
    scale_factor = 50.0  # Uniform point size

    # Plot all points with uniform size and color mapped by intensity
    pts = mlab.points3d(xs, ys, zs, normalized_intensities, scale_factor=scale_factor, figure=fig, colormap='viridis')

    # Highlight the origin (0, 0, 0) with the same size but different color
    mlab.points3d(0, 0, 0, color=(1, 0, 0), scale_factor=scale_factor)

    # Add a colorbar to represent intensity values
    mlab.colorbar(pts, title='Intensity', orientation='vertical', nb_labels=5)

    # Adjust the view to show a perspective projection
    mlab.view(azimuth=45, elevation=80, distance=15)

    mlab.show()

# Lattice parameters
a, b, c = 26.03, 30.63, 32.91
alpha, beta, gamma = 88.320, 108.710, 111.840

# Example usage
file_path = '/mnt/f/Lysozyme highISA_dry_data/90_6beta_2alpha/all.hkl'
data = read_data(file_path)
transform_matrix = lattice_transform(a, b, c, alpha, beta, gamma)
transformed_data = transform_points(data, transform_matrix)
plot_data(transformed_data)
