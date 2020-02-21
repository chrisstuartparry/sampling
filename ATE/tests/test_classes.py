'''
Simple tests and data generation.
'''

from .. import UniformSamplingStrategy, Domain, Samplerun
import os


def test_samplerun():
    '''
    Sets up uniform geemeration of data points and csv output.
    '''

    numsamples = 5
    domain = Domain()
    sampling_strategy = UniformSamplingStrategy()

    run1 = Samplerun(numsamples, domain, sampling_strategy)
    run1.perform_sample(out_file='100uniform.csv')


if __name__ == '__main__':
    test_samplerun()
