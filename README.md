# balanced_spiking_network

A Python package for simulating balanced spiking neural networks.

## Installation


pip install git+ssh://git@github.com/yourusername/balanced_spiking_network.git

## Usage

Run the simulation from the command line:

bsn --duration 1000 --output spikes.pkl --seed 42


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