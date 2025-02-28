import argparse
import pickle
import numpy as np
from .network import BalancedSpikingNetwork
from .simulation import SimulationEngine
from .io import InputSystem


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

def main():
    parser = argparse.ArgumentParser(
        description="Run balanced spiking network simulation"
    )
    parser.add_argument("-d", "--duration", type=float, default=1000.0,
                        help="Simulation duration in ms")
    parser.add_argument("-o", "--output", type=str, default="spikes.pkl",
                        help="Output spike data file (pickle format)")
    parser.add_argument("--mu_zero", type=float, default=15.1,
                        help="External constant input")
    parser.add_argument("--V_th_std", type=float, default=0.0,
                        help="Threshold Potential standard deviation")
    parser.add_argument("--N", type=int, default=10000,
                        help="Total number of neurons in the network")
    parser.add_argument("--C", type=int, default=1000,
                        help="Number of connections per neuron")
    parser.add_argument("--f", type=float, default=0.8,
                        help="Ratio of excitatory to inhibitory neurons")
    parser.add_argument("--g", type=float, default=5,
                        help="Relative strength of inhibitory synapses compared to excitatory synapses")
    parser.add_argument("--tau_m", type=float, default=10.0,
                        help="Membrane time constant")
    parser.add_argument("--V_th_mean", type=float, default=-55.0,
                        help="Mean threshold potential for spiking")
    parser.add_argument("--J_mean", type=float, default=1e-3,
                        help="Mean synaptic weight for excitatory synapses")
    parser.add_argument("--dt", type=float, default=0.1,
                        help="Simulation time step")
    parser.add_argument("--burn_in", type=float, default=0.0,
                        help="Burn in time for the simulation to remove the transients")
    parser.add_argument("--session", type=int, default=0,
                        help="Session number for RNG")
    parser.add_argument("--trial", type=int, default=0,
                        help="Trial number for RNG")
    parser.add_argument("--mu_1", choices=['none', 'sine', 'bumps'], default='none',
                        help="Type of mu_1 input (none, sine, or bumps)")
    parser.add_argument("--mu_2", choices=['none', 'sine', 'bumps'], default='none',
                        help="Type of mu_2 input (none, sine, or bumps)")

    args = parser.parse_args()

    # Initialize network
    net = BalancedSpikingNetwork(N=args.N, C=args.C, f=args.f, g=args.g,
                                 tau_m=args.tau_m, V_th_mean=args.V_th_mean,
                                 V_th_std=args.V_th_std, J_mean=args.J_mean,
                                 mu_zero=args.mu_zero, dt=args.dt,
                                 session=args.session, trial=args.trial)


    # Initialize input system
    input_system = InputSystem(net)
    net.input_neurons = input_system.select_input_neurons()

    # Generate mu_1 and mu_2 based on command-line arguments
    mu_1 = None
    mu_2 = None

    if args.mu_1 == 'sine':
        mu_1 = generate_input_sine(net.rng_input, args.duration, len(net.input_neurons[0]), args.dt)
    elif args.mu_1 == 'bumps':
        mu_1 = generate_input_bumps(net.rng_input, args.duration, len(net.input_neurons[0]), args.dt)

    if args.mu_2 == 'sine':
        mu_2 = generate_input_sine(net.rng_input, args.duration, len(net.input_neurons[1]), args.dt)
    elif args.mu_2 == 'bumps':
        mu_2 = generate_input_bumps(net.rng_input, args.duration, len(net.input_neurons[1]), args.dt)

    # Initialize simulation engine
    engine = SimulationEngine(net)

    # Run simulation
    spikes = engine.run(args.duration, T_burn_in=args.burn_in, record_spikes=True, mu_1=mu_1, mu_2=mu_2)

    data_to_save = {"spikes":spikes,
                    "input_1_neurons":net.input_neurons[0],
                    "input_2_neurons":net.input_neurons[1],
                    "rng_check":net.rng[3].normal(0, 1, 3)}

    # Save results
    save_spikes(data_to_save, args.output)

def save_spikes(spikes, filename):
    """Save spike times to a pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(spikes, f)

if __name__ == "__main__":
    main()
