# balanced_spiking_network

[![License](https://img.shields.io/badge/license-GNU%20GPL%20v3.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)]()

## Overview

`balanced_spiking_network` is a Python package designed for simulating balanced spiking neural networks. It provides a modular framework for creating, simulating, and analyzing these networks, which are composed of leaky integrate-and-fire (LIF) neurons. The package is suitable for researchers and students interested in computational neuroscience, neural network modeling, and related fields.

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## Key Features

-   **Modular Design:** Easily create and customize different components of your spiking neural network.
-   **LIF Neurons:** Simulate networks with Leaky Integrate-and-Fire neurons.
-   **Balanced Networks:** Study network dynamics and stability in balanced excitatory-inhibitory networks.
-   **Configurable Parameters:** Define and adjust network parameters, inputs, and simulation settings.
-   **Command-Line Interface (CLI):** Run simulations and analyses directly from the command line.

## Installation

To install the `balanced_spiking_network` package, run:
```
!pip install git+ssh://git@github.com/fraziphy/balanced_spiking_network.git
```

This command installs the package and its dependencies. Make sure you have Python 3.7 or higher installed.

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

To **uninstall** the module, please copy and execute the following command in a single cell:

```
!python -m pip uninstall balanced_spiking_network --yes
```

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## Usage

Here's a basic example of how to use the package:

```
from balanced_spiking_network import network, simulation, inputs
```

Create a network

```
net = network.Network()
```

Define input stimuli

```
input_signal = inputs.ConstantInput(rate=10)
```

Simulate the network

```
sim = simulation.Simulation(network=net, input=input_signal, duration=1000)
results = sim.run()
```

### Command-Line Interface (CLI)

The package also provides a CLI for running simulations. Run the simulation from the command line for a network subject to constant input of 18 mV for 100 ms for the trial number one and store the data as spikes.pkl:

bsn --duration 100 --mu_zero 18 --output spikes.pkl --trial 1


For help on available options:

bsn --help


------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## The structure of the project is as follows:
```
balanced_spiking_network/
├── balanced_spiking_network/
│ ├── init.py
│ ├── network.py # Defines the Network class.
│ ├── parameters.py # Handles network parameters.
│ ├── simulation.py # Implements simulation routines.
│ ├── inputs.py # Defines input stimuli.
│ ├── cli.py # Command-line interface.
│ ├── utilities.py # Utility functions.
├── setup.py # Installation script.
└── README.md # This file.

```

-   `balanced_spiking_network/network.py`: Defines the `Network` class for creating spiking neural networks.
-   `balanced_spiking_network/parameters.py`: Manages network parameters and settings.
-   `balanced_spiking_network/simulation.py`: Implements the simulation routines.
-   `balanced_spiking_network/inputs.py`: Defines various input stimuli that can be applied to the network.
-   `balanced_spiking_network/cli.py`: Provides a command-line interface for running simulations.
-   `balanced_spiking_network/utilities.py`: Contains utility functions used throughout the package.
-   `setup.py`:  The installation script for the package.
-   `README.md`: Provides an overview of the project and instructions for installation and usage.

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## Contributing

Thank you for considering contributing to our project! We welcome contributions from the community to help improve our project and make it even better. To ensure a smooth contribution process, please follow these guidelines:

1. **Fork the Repository**: Fork our repository to your GitHub account and clone it to your local machine.

2. **Branching Strategy**: Create a new branch for your contribution. Use a descriptive branch name that reflects the purpose of your changes.

3. **Code Style**: Follow our coding standards and style guidelines. Make sure your code adheres to the existing conventions to maintain consistency across the project.

4. **Pull Request Process**:
    Before starting work, check the issue tracker to see if your contribution aligns with any existing issues or feature requests.
    Create a new branch for your contribution and make your changes.
    Commit your changes with clear and descriptive messages explaining the purpose of each commit.
    Once you are ready to submit your changes, push your branch to your forked repository.
    Submit a pull request to the main repository's develop branch. Provide a detailed description of your changes and reference any relevant issues or pull requests.

5. **Code Review**: Expect feedback and review from our maintainers or contributors. Address any comments or suggestions provided during the review process.

6. **Testing**: Ensure that your contribution is properly tested. Write unit tests or integration tests as necessary to validate your changes. Make sure all tests pass before submitting your pull request.

7. **Documentation**: Update the project's documentation to reflect your changes. Include any necessary documentation updates, such as code comments, README modifications, or user guides.

8. **License Agreement**: By contributing to our project, you agree to license your contributions under the terms of the project's license (GNU General Public License v3.0).

9. **Be Respectful**: Respect the opinions and efforts of other contributors. Maintain a positive and collaborative attitude throughout the contribution process.

We appreciate your contributions and look forward to working with you to improve our project! If you have any questions or need further assistance, please don't hesitate to reach out to us.

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## Credits

- **Author:** [Farhad Razi](https://github.com/fraziphy)

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE)

------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

## Contact

- **Contact information:** [email](farhad.razi.1988@gmail.com)
# _**Linear_decoder.py**_
