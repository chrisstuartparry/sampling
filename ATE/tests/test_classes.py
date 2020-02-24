'''
Simple tests and data generation.
'''

from .. import UniformSamplingStrategy, Domain, Samplerun
import os


def test_samplerun():
    '''
    Sets up uniform geemeration of data points and csv output.
    '''

    n_samples = 5

    run1 = Samplerun()
    run1.perform_sample(out_file='100uniform.csv',
                        n_samples=n_samples,
                        domain=Domain(),
                        sampling_strategy=UniformSamplingStrategy())


if __name__ == '__main__':
    test_samplerun()
