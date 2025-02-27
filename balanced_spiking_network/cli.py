import argparse
import pickle
import numpy as np
from .network import BalancedSpikingNetwork
from .simulation import SimulationEngine
from .io import InputSystem

def main():
    parser = argparse.ArgumentParser(
        description="Run balanced spiking network simulation"
    )
    parser.add_argument("-d", "--duration", type=float, default=1000.0,
                        help="Simulation duration in ms")
    parser.add_argument("-o", "--output", type=str, default="spikes.pkl",
                        help="Output spike data file (pickle format)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility")
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

    args = parser.parse_args()

    # Initialize network
    net = BalancedSpikingNetwork(N=args.N, C=args.C, f=args.f, g=args.g,
                                 tau_m=args.tau_m, V_th_mean=args.V_th_mean,
                                 V_th_std=args.V_th_std, J_mean=args.J_mean,
                                 mu_zero=args.mu_zero, dt=args.dt,
                                 rng_seed=args.seed)
    net.reset_state() #call the function for the updated parameter

    # Initialize input system
    net.input_neurons = InputSystem(net).select_input_neurons()

    # Initialize simulation engine
    engine = SimulationEngine(net)

    # Run simulation
    spikes = engine.run(args.duration, T_burn_in=args.burn_in, record_spikes=True)

    # Save results
    save_spikes(spikes, args.output)


def save_spikes(spikes, filename):
    """Save spike times to a pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(spikes, f)
