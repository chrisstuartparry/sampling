import numpy as np


class Parameter:
    '''
    Holds name, acceptable values, (and sampling distribution) for an input parameter.
    '''

    def __init__(self, name, valuerange=[], values=[]):
        self.name = name
        if len(values) == 0:
            self.val = valuerange
            self.discrete = False
        else:
            self.val = values
            self.discrete = True

    def gen_uniform(self, num):
        '''
        Generates appropriate uniform random data (either discrete or cont) for parameter.
        '''

        if self.discrete:
            scope = len(self.val)
            if num == 1:
                return self.val[np.random.randint(scope)]
            else:
                return [self.val[np.random.randint(scope)] for i in range(num)]

        else:
            return np.random.uniform(self.val[0], self.val[1], num)
