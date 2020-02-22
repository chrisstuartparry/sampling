from ATE import UniformSamplingStrategy, Domain
import numpy as np


def generate_params():
    n_batches = 100
    n_samples_per_batch = 1000
    seed = 1

    print('Seed is %d' % seed)
    print('Each batch will contain %d samples' % n_samples_per_batch)

    np.random.seed(seed)

    domain = Domain()
    sampling_strategy = UniformSamplingStrategy()

    for batch_idx in range(n_batches):
        df = domain.gen_data_frame(sampling_strategy, n_samples_per_batch)
        df.to_csv('output/run0/batch%d_in.csv' % batch_idx, index=False)

        if batch_idx % 10 == 0:
            print('Generated batch %d of %d' % (batch_idx + 1, n_batches))


if __name__ == '__main__':
    generate_params()
