from ATE import UniformSamplingStrategy, Domain
import numpy as np


def test_generate_params():
    '''
    Sets up uniform generation of data points and csv output.
    '''

    n_samples = 1000
    seed = 1

    np.random.seed(seed)

    domain = Domain()
    sampling_strategy = UniformSamplingStrategy()
    df = domain.gen_data_frame(sampling_strategy, n_samples)
    df.to_csv('params/1000params.csv', index=False)
    
    
def test_gp_dfixed():
    '''
    Sets up uniform generation with all discrete parameters fixed to set values.
    '''

    n_samples = 100
    seed = 2

    np.random.seed(seed)

    domain = Domain()
    sampling_strategy = UniformSamplingStrategy()
    
    domain.fix_param(domain.params[1], 'tungsten')
    domain.fix_param(domain.params[2], 'SiC')
    domain.fix_param(domain.params[3], 'H2O')
    domain.fix_param(domain.params[5], 'SiC')
    domain.fix_param(domain.params[6], 'Li4SiO4')
    domain.fix_param(domain.params[7], 'Be')
    domain.fix_param(domain.params[8], 'H20')
    
    df = domain.gen_data_frame(sampling_strategy, n_samples)
    df.to_csv('params/100params0000000.csv', index=False)



if __name__ == '__main__':
    test_gp_dfixed()
