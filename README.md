# balanced_spiking_network

A Python package for simulating balanced spiking neural networks.

## Installation


pip install git+ssh://git@github.com/fraziphy/balanced_spiking_network.git

!python -m pip uninstall balanced_spiking_network.git --yes

## Usage

Run the simulation from the command line:

bsn --duration 100 --mu_1 sine --output spikes_sine.pkl --trial 1


For help on available options:

bsn --help



balanced_spiking_network/
├── __init__.py
├── network.py
├── connectivity.py
├── parameters.py
├── simulation.py
├── io.py
├── cli.py
├── utilities.py
├── setup.py
└── README.md