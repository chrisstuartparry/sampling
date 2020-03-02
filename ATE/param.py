class Parameter:
    '''
    All parameters derive from this class.
    '''

    def __init__(self, name, human_readable_name):
        self.name = name
        self.human_readable_name = human_readable_name


class DiscreteParameter(Parameter):
    '''
    Holds name and acceptable values for a discrete input parameter.
    '''

    def __init__(self, name, human_readable_name, values):
        Parameter.__init__(self, name, human_readable_name)
        self.val = values

    def gen(self, strategy, num):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        return {self.name: strategy.gen_discrete(self, num)}

    def fix(self, value):
        return {self.name: value}

    def transform_columns(self):
        '''
        Get column names for transformed representation.
        '''
        return ['%s_%s' % (self.name, val) for val in self.val]


class ContinuousParameter(Parameter):
    '''
    Holds name and sampling distribution for a continuous input parameter.
    '''

    def __init__(self, name, human_readable_name, low, high):
        Parameter.__init__(self, name, human_readable_name)
        self.val = [low, high]

    def gen(self, strategy, num):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        return {self.name: strategy.gen_continuous(self, num)}

    def fix(self, value):
        return {self.name: value}

    def transform_columns(self):
        '''
        Get column names for transformed representation.
        '''
        return [self.name]


class SumParameterGroup(Parameter):
    '''
    Holds name and sampling distribution for a group of continuous input parameters that sum to a constant total.
    '''

    def __init__(self, name, human_readable_name, names, total):
        Parameter.__init__(self, name, human_readable_name)
        self.names = [name for (name, human_name) in names]
        self.human_readable_names = [
            human_name for (name, human_name) in names]
        self.total = total
        self.size = len(names)

    def gen(self, strategy, num):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        generated = strategy.gen_sum(self, num)
        return {name: generated[:, i].tolist() for i, name in enumerate(self.names)}

    def fix(self, value):
        return value

    def transform_columns(self):
        '''
        Get column names for transformed representation.
        '''
        return self.names
