import numpy as np

def generate_input_sine(rng, duration_ms, n_input_neurons, dt, amplitude=2, noise_std=0.2):
    """
    Generate sinusoidal current with Gaussian noise for input neurons.

    Parameters:
    duration_ms (float): Duration of the simulation in milliseconds
    input_neurons_dyn (numpy.ndarray): Array of neuron indices receiving dynamic input
    amplitude (float): Amplitude of the sine wave (default: 0.5)
    noise_std (float): Standard deviation of the Gaussian noise (default: 0.1)

    Returns:
    numpy.ndarray: Normalized current for each input neuron

    Global variables used:
    dt (float): Time step in milliseconds
    """
    num_samples = int(duration_ms / dt)
    time = np.arange(num_samples) * dt

    # Generate base sine wave with a period of 400 ms
    frequency = 2.5  # 2.5 Hz for 400 ms period
    base_sine = amplitude * np.sin(2 * np.pi * frequency * time / 1000)

    # Keep only the upper half of the sine wave
    current = np.maximum(base_sine, 0)

    # current = np.repeat(current.reshape(1,-1), n_input_neurons, axis=0)

     # Generate unique Gaussian noise for each neuron and add to sine wave
    current = current + rng.normal(0, noise_std, (n_input_neurons,num_samples))


    return current






def generate_input_bumps(rng, duration_ms, n_input_neurons, dt, noise_std=0.2):
    """
    Generate a potential with two large bumps at the edges and a smaller, lower bump in the middle.

    Parameters:
    x: array of x values
    a: controls the position of the bumps
    b: controls the width of the potential
    max_height: height of the outer peaks
    mid_height: height of the middle peak (should be less than max_height)
    dip: how much to pull down the middle section
    """
    a=1.0
    b=2.0
    max_height=3.0
    mid_height=0.8
    dip=0.3

    num_samples = int(duration_ms / dt)
    x = np.linspace(-2, 2, num_samples)
    # Ensure mid_height is less than max_height
    mid_height = min(mid_height, max_height - 0.5)

    # Create the basic shape with three bumps
    V = max_height * (np.exp(-(x+a)**2/0.4) + np.exp(-(x-a)**2/0.2)) + mid_height * np.exp(-x**2/0.4)

    # Pull down the middle section
    # V -= dip * np.exp(-x**2/40)

    # Ensure it goes to zero at the edges
    V *= (1 - (x/b)**2)**2

    # Normalize to ensure max_height is reached
    V *= max_height / np.max(V)

    # Ensure no negative values
    V = np.maximum(V, 0)

    current = V + rng.normal(0, noise_std, (n_input_neurons, num_samples))

    return current
