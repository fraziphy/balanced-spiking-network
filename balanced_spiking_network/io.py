import numpy as np

class InputSystem:
    """Manage input neuron selection"""

    def __init__(self, network):
        self.network = network
        self.rng = network.rng
        self.input_neurons = self.select_input_neurons()

    def select_input_neurons(self, overlap=0.1, new=0.2):
        """Select overlapping and novel input populations"""
        N = self.network.N
        N_E = int(self.network.f * N)  # Directly calculate N_E
        n_input_const_E = int(0.3 * N_E)
        n_input_const_I = int(0.3 * (N - N_E))
        input_1_neurons = np.concatenate([
            self.rng[2].choice(N_E, n_input_const_E, replace=False),
            N_E + self.rng[2].choice(N - N_E, n_input_const_I, replace=False)
        ])

        n_overlap_E = int(0.1 * N_E)
        n_overlap_I = int(0.1 * (N - N_E))
        n_new_E = int(0.2 * N_E)
        n_new_I = int(0.2 * (N - N_E))

        overlap_E = self.rng[2].choice(input_1_neurons[input_1_neurons < N_E], n_overlap_E, replace=False)
        overlap_I = self.rng[2].choice(input_1_neurons[input_1_neurons >= N_E], n_overlap_I, replace=False)
        new_E = self.rng[2].choice(np.setdiff1d(np.arange(N_E), input_1_neurons), n_new_E, replace=False)
        new_I = self.rng[2].choice(np.setdiff1d(np.arange(N_E, N), input_1_neurons), n_new_I, replace=False)

        input_2_neurons = np.concatenate([overlap_E, overlap_I, new_E, new_I])

        return input_1_neurons, input_2_neurons
