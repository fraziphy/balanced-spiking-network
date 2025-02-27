class NeuralParameters:
    """Container for biological parameters"""

    def __init__(self):
        # Membrane properties
        self.E_L = -70.0    # Resting potential (mV)
        self.V_r = -75.0    # Reset potential (mV)
        self.tau_m = 10.0   # Membrane time constant (ms)
        self.tau_r = 2.0    # Refractory period (ms)

        # External inputs
        self.mu_zero = 15.1    # Baseline current (pA)
        self.dt = 0.1         # Time step (ms)
