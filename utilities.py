import numpy as np

def generate_heterogeneous_thresholds(V_th_mean, V_th_std, rng, N):
    """
    Generate heterogeneous threshold potentials for N neurons.
    """
    if V_th_std == 0:
        V_th = np.full(N, V_th_mean)
    else:
        V_th = rng.uniform(V_th_mean - V_th_std * np.sqrt(3),
                           V_th_mean + V_th_std * np.sqrt(3), N)
    return V_th
