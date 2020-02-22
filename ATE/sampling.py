from numpy import ones
from numpy.random import randint, uniform, dirichlet


class UniformSamplingStrategy:
    '''
    Samples data from the uniform distribution
    '''

    def gen_discrete(self, param, num):
        '''
        Generates appropriate uniform random data for a discrete parameter.
        '''

        scope = len(param.val)
        if num == 1:
            return param.val[randint(scope)]
        else:
            return [param.val[randint(scope)] for i in range(num)]

    def gen_continuous(self, param, num):
        '''
        Generates appropriate uniform random data for a continuous parameter.
        '''

        return uniform(param.val[0], param.val[1], num).tolist()

    def gen_sum(self, param, num):
        '''
        Generates appropriate uniform random data for a group of parameters.
        '''

        return param.total * dirichlet(ones(4), size=num)
