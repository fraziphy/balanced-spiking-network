import numpy as np
from .parameters import NeuralParameters


def generate_heterogeneous_thresholds(V_th_mean, V_th_std, N, rng, distribution="uniform"):
    """
    Generate threshold potentials ensuring V_th > V_r.

    Args:
        V_th_mean: Mean threshold potential
        V_th_std: Standard deviation of thresholds
        N: Number of neurons
        rng: Random number generator
        distribution: "uniform" or "normal" (default: "uniform")

    Returns:
        np.ndarray: Threshold potentials that are strictly greater than V_r
    """
    # Get reset potential from parameters
    params = NeuralParameters()
    V_r = params.V_r
    eps = 1e-9  # Small offset to ensure strict inequality

    # Handle zero standard deviation case first (distribution irrelevant)
    if V_th_std == 0:
        V_th = np.full(N, V_th_mean)
    else:
        # Generate based on specified distribution
        if distribution == "uniform":
            a = V_th_mean - V_th_std * np.sqrt(3)
            b = V_th_mean + V_th_std * np.sqrt(3)
            V_th = rng.uniform(a, b, N)
        elif distribution == "normal":
            V_th = rng.normal(V_th_mean, V_th_std, N)
        else:
            raise ValueError(f"Invalid distribution: {distribution}. Use 'uniform' or 'normal'")

    # Ensure all thresholds are strictly above V_r (applies to all cases)
    V_th = np.clip(V_th, V_r + eps, None)

    return V_th




def create_connectivity_matrix(N, N_E, C_E, C_I, mean_weight, g, rng):
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



def select_input_neurons(N, N_E, portion, overlap, rng):
    """
    Select neurons to receive constant and dynamic inputs.

    Parameters:
    rng (numpy.random.Generator): Random number generator

    Returns:
    tuple: (input_1_neurons, input_2_neurons)
        input_1_neurons (numpy.ndarray): Indices of neurons receiving constant input
        input_2_neurons (numpy.ndarray): Indices of neurons receiving dynamic input

    Global variables used:
    N (int): Total number of neurons
    N_E (int): Number of excitatory neurons
    """
    n_input_const_E = int(portion * N_E)
    n_input_const_I = int(portion * (N - N_E))
    input_1_neurons = np.concatenate([
        rng.choice(N_E, n_input_const_E, replace=False),
        N_E + rng.choice(N - N_E, n_input_const_I, replace=False)
    ])

    n_overlap_E = int(overlap * N_E)
    n_overlap_I = int(overlap * (N - N_E))
    n_new_E = int(( portion-overlap ) * N_E)
    n_new_I = int(( portion-overlap ) * (N - N_E))

    overlap_E = rng.choice(input_1_neurons[input_1_neurons < N_E], n_overlap_E, replace=False)
    overlap_I = rng.choice(input_1_neurons[input_1_neurons >= N_E], n_overlap_I, replace=False)
    new_E = rng.choice(np.setdiff1d(np.arange(N_E), input_1_neurons), n_new_E, replace=False)
    new_I = rng.choice(np.setdiff1d(np.arange(N_E, N), input_1_neurons), n_new_I, replace=False)

    input_2_neurons = np.concatenate([overlap_E, overlap_I, new_E, new_I])

    return input_1_neurons, input_2_neurons
