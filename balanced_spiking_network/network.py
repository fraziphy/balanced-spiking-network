import numpy as np
from .connectivity import create_connectivity_matrix
from .parameters import NeuralParameters
from .utilities import generate_heterogeneous_thresholds

class BalancedSpikingNetwork:
    """Main network class"""

    def __init__(self, N=10000, C=1000, f=0.8, g=5,
                 tau_m=10.0, V_th_mean=-55.0,
                 V_th_std=0.0, # Added V_th_std to init
                 J_mean = 1e-3,
                 mu_zero = 15.1, # Added mu_zero to init
                 dt = 0.1, # Added dt to init
                 session = 0,
                 trial = 0):

        # Initialize parameters
        self.params = NeuralParameters()
        self.N = N
        self.C = C
        self.f = f
        self.g = g
        self.tau_m = tau_m
        self.V_th_mean = V_th_mean
        self.V_th_std = V_th_std # Store V_th_std
        self.J_mean = J_mean
        self.params.mu_zero = mu_zero #initializes it in the params here
        self.params.dt = dt #initializes dt in the params here

        # Derived parameters
        self.N_E = int(f * N)
        self.C_E = int(f * C)
        self.C_I = C - self.C_E

        # Random state management
        self.rng_init = np.random.default_rng(np.random.SeedSequence(entropy=654321, spawn_key=(0, session, 1, trial)))
        self.rng = [np.random.default_rng(np.random.SeedSequence(entropy=654321, spawn_key=(0, session, 0, i))) for i in range(4)]
        self.rng_input = np.random.default_rng(np.random.SeedSequence(entropy=654321, spawn_key=(0, session, 2, trial)))
        # rng_init for initial states different across trials and sessions
        # rng[0] is used for generating thresholds, rng[1] for connectivity,
        # rng[2] for ID of stimulated neurons, rng[3] for RNG check
        # rng_input for inputs across trials

        # Network state
        self.V = None
        self.V_th = None
        self.last_spike = None
        self.refractory = None
        self.connectivity = None
        self.input_neurons = None

        # Initialize network
        self.reset_state()

    def reset_state(self):
        """Reset network to initial conditions"""
        self.V = self.rng_init.uniform(self.params.V_r,
                                self.V_th_mean,
                                self.N)
        self.V_th = generate_heterogeneous_thresholds(
            self.V_th_mean, self.V_th_std, self.rng[0], self.N # Used stored V_th_std
        )
        self.last_spike = np.full(self.N, -np.inf)
        self.refractory = np.zeros(self.N, dtype=bool)
        self.connectivity = create_connectivity_matrix(
            N = self.N,
            N_E = self.N_E,
            C_E = self.C_E,
            C_I = self.C_I,
            mean_weight=self.J_mean,
            rng=self.rng[1],
            g=self.g
        )

    def set_state(self, state):
        self.V, self.last_spike, self.refractory = state

    def get_params(self):
        """Return the network parameters."""
        return self.params
