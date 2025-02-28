import numpy as np

class SimulationEngine:
    """Handle numerical integration"""

    def __init__(self, network):
        self.net = network
        self.params = network.get_params()
        self.dt = network.params.dt

    def run(self, T_sim, T_burn_in=0.0, record_spikes=False, mu_1=None, mu_2=None):
        """Execute simulation loop with burn-in period."""

        # **1. Burn-in Period (Transient State Removal)**
        if T_burn_in > 0:
            self._simulate(T_burn_in, record_spikes=False, mu_1=None, mu_2=None)  # No recording during burn-in
        # **2. Recording Period**
        final_state, spikes = self._simulate(T_sim, record_spikes=record_spikes, mu_1=mu_1, mu_2=mu_2) #simulation call returns

        return spikes

    def _simulate(self, T_sim, record_spikes=False, mu_1=None, mu_2=None):
        """Core simulation loop (private method)."""
        spikes = []
        V, last_spike, refractory = self.net.V, self.net.last_spike, self.net.refractory
        V_th = self.net.V_th
        W = self.net.connectivity
        input_1_neurons, input_2_neurons = self.net.input_neurons

        for t in np.arange(0, T_sim, self.dt):
            refractory = (t - last_spike) <= self.params.tau_r
            synaptic_input = self.params.tau_m * np.dot(W, (last_spike == t - self.dt).astype(float)) / self.dt

            # Apply constant input to all neurons
            external_input = np.full(self.net.N, self.params.mu_zero, dtype=float)

            # Apply additional dynamic input to selected neurons, if mu is provided
            if mu_1 is not None:
                external_input[input_1_neurons] += mu_1[:, int(t/self.dt)]
            if mu_2 is not None:
                external_input[input_2_neurons] += mu_2[:, int(t/self.dt)]

            dV = np.where(refractory, 0, (-(V - self.params.E_L) + synaptic_input + external_input) / self.params.tau_m)
            V += dV * self.dt

            spiked = (V >= V_th) & ~refractory
            if np.sum(spiked) > 0:
                V[spiked] = self.params.V_r
                last_spike[spiked] = t
                if record_spikes:
                    spikes.extend([(t, i) for i in np.where(spiked)[0]])

            V[refractory] = self.params.V_r

        # Adjust last_spike times for the next phase of simulation
        last_spike = np.where(last_spike < T_sim, last_spike - T_sim, -np.inf)

        final_state = (V, last_spike, refractory)
        self.net.set_state(final_state)  #update network state

        if record_spikes:
            return final_state, spikes
        else:
            return final_state, []  # Return empty spike list
