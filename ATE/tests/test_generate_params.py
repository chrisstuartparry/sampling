from .. import UniformSamplingStrategy, Domain
import numpy as np


def test_generate_params():
    '''
    Sets up uniform geemeration of data points and csv output.
    '''

    n_samples = 1000
    seed = 1

    np.random.seed(seed)

    domain = Domain()
    sampling_strategy = UniformSamplingStrategy()
    df = domain.gen_data_frame(sampling_strategy, n_samples)
    df.to_csv('output/1000params.csv', index=False)
