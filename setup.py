from setuptools import setup, find_packages

setup(
    name='balanced_spiking_network',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'bsn = balanced_spiking_network.cli:main'
        ]
    },
    author='Farhad Razi',
    author_email='farhad.razi.1988@gmail.com',
    description='A balanced spiking neural network simulation package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/balanced_spiking_network',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose appropriate license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Or your minimum required Python version
)
