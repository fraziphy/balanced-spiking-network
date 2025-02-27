import numpy as np

def create_connectivity_matrix(N, N_E, C_E, C_I, mean_weight, rng, g):
    """
    Create a connectivity matrix for a neural network.

    Parameters:
    rng (numpy.random.Generator): Random number generator
    mean_weight (float): Mean synaptic weight

    Returns:
    numpy.ndarray: NxN connectivity matrix where N is the total number of neurons

    Global variables used:
    N (int): Total number of neurons
    N_E (int): Number of excitatory neurons
    C_E (int): Number of excitatory connections per neuron
    C_I (int): Number of inhibitory connections per neuron
    g (float): Relative strength of inhibitory to excitatory synapses
    """
    W = np.zeros((N, N))

    exc_weight = mean_weight
    inh_weight = -mean_weight * g

    for i in range(N):
        if i < N_E:  # Excitatory neuron
            # Select random excitatory and inhibitory connections
            exc_connections = rng.choice(N_E, C_E, replace=False)
            inh_connections = rng.choice(range(N_E, N), C_I, replace=False)

            # Assign constant weights
            W[i, exc_connections] = exc_weight
            W[i, inh_connections] = inh_weight

        else:  # Inhibitory neuron
            # Select random excitatory and inhibitory connections
            exc_connections = rng.choice(N_E, C_E, replace=False)
            inh_connections = rng.choice(range(N_E, N), C_I, replace=False)

            # Assign constant weights
            W[i, exc_connections] = exc_weight
            W[i, inh_connections] = inh_weight

    return W
