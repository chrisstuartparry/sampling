'''
Simple tests and data generation.
'''

from ATE import UniformSamplingStrategy, Domain, Samplerun
import os
import pandas as pd


def test_samplerun():
    '''
    Sets up uniform generation of data points and csv output.
    '''

    n_samples = 5

    run1 = Samplerun()
    run1.perform_sample(out_file='100uniform.csv',
                        n_samples=n_samples,
                        domain=Domain(),
                        sampling_strategy=UniformSamplingStrategy())
                        
def test_runfromfile():
    '''
    Sets up uniform generation of data points and csv output.
    '''

    n_samples = 100

    run1 = Samplerun()
    run1.perform_sample(out_file='100fix0000000out.csv',
                        n_samples=n_samples,
                        param_values=pd.read_csv("params/100params0000000.csv"),
                        domain=Domain(),
                        sampling_strategy=UniformSamplingStrategy())


if __name__ == '__main__':
    test_runfromfile()
