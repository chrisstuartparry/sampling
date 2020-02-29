TBR Sampling
============

This repository contains implementation of batch sampling of the TBR Monte Carlo simulation. The process is divided into two stages, wherein the first stage produces a batch of data points from the TBR parameter domain, and the second stage orchestrates dockerized Monte Carlo simulation to evaluate TBR at each data point. Due to possibly computationally intensive aspect of the process, scripts are included to allow deployment on SLURM-managed clusters using Singularity.


Usage
-----

The repository provides the `ATE` Python package. Use `pip` to install it on your system.


Install Instructions
--------------------

> Run "pip3 install ./" in top directory.
> Run "python3 ATE/tests/test_classes.py" to generate data points.
>> If docker openmcworkshop/find-tbr is not already running, the Samplerun.perform_sample method will start it in silent console mode.
> Check output csvs in ATE/tests/output/<name>.csv
>> tbr and tbr_error are in the rightmost columns of these output csvs


License
-------

This work was realised in 2020 as a group project at University College London with the support from UKAEA. The authors of the implementation are Petr Mánek and Graham Van Goffrier.

Permission to use, distribute and modify is hereby granted in accordance with the MIT License. See the LICENSE file for details.
