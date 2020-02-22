import pandas as pd


class Parameter:
    '''
    All parameters derive from this class.
    '''

    def __init__(self, name):
        self.name = name


class DiscreteParameter(Parameter):
    '''
    Holds name and acceptable values for a discrete input parameter.
    '''

    def __init__(self, name, values):
        Parameter.__init__(self, name)
        self.val = values

    def gen(self, strategy, num):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        return strategy.gen_discrete(self, num)

    def transform_columns(self):
        '''
        Get column names for transformed representation.
        '''
        return ['%s_%s' % (self.name, val) for val in self.val]


class ContinuousParameter(Parameter):
    '''
    Holds name and sampling distribution for a continuous input parameter.
    '''

    def __init__(self, name, low, high):
        Parameter.__init__(self, name)
        self.val = [low, high]

    def gen(self, strategy, num):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        return strategy.gen_continuous(self, num)

    def transform_columns(self):
        '''
        Get column names for transformed representation.
        '''
        return [self.name]


class Domain:
    '''
    Holds all parameters of the model.
    '''

    def __init__(self):
        '''
        Generates array of input parameters for model in use.
        '''
        FWT = ContinuousParameter('firstwall_thickness', 0, 20)
        FWAM = DiscreteParameter('firstwall_amour_material', ['tungsten'])
        FWSM = DiscreteParameter(
            'firstwall_structural_material', ['SiC', 'eurofer'])
        FWCM = DiscreteParameter(
            'firstwall_coolant_material', ['H2O', 'He', 'D2O'])
        BLT = ContinuousParameter('blanket_thickness', 0, 500)
        BSM = DiscreteParameter(
            'blanket_structural_material', ['SiC', 'eurofer'])
        BBM = DiscreteParameter('blanket_breeder_material', [
                                'Li4SiO4', 'Li2TiO3'])
        BMM = DiscreteParameter(
            'blanket_multiplier_material', ['Be', 'Be12Ti'])
        BCM = DiscreteParameter(
            'blanket_coolant_material', ['H2O', 'He', 'D2O'])
        BBEF = ContinuousParameter(
            'blanket_breeder_li6_enrichment_fraction', 0, 1)
        BBPF = ContinuousParameter('blanket_breeder_packing_fraction', 0, 1)
        BMPF = ContinuousParameter(
            'blanket_multiplier_packing_fraction', 0, 1)
        BMF = ContinuousParameter('blanket_multiplier_fraction', 0, 1)
        BBF = ContinuousParameter('blanket_breeder_fraction', 0, 1)
        BSF = ContinuousParameter('blanket_structural_fraction', 0, 1)
        BCF = ContinuousParameter('blanket_coolant_fraction', 0, 1)

        self.params = [FWT, FWAM, FWSM, FWCM, BLT, BSM, BBM,
                       BMM, BCM, BBEF, BBPF, BMPF, BMF, BBF, BSF, BCF]
        self.numparams = len(self.params)
        self.fixed_params = {}

    def create_data_frame(self):
        '''
        Create empty data frame with headers for all model parameters.
        '''
        return pd.DataFrame(
            columns=[param.name for param in self.params]
        )

    def gen_param_values(self, param, strategy, num):
        '''
        Generate requested number of values for a single parameter using specified sampling strategy.
        '''
        if param.name in self.fixed_params:
            return self.fixed_params[param.name]
        else:
            return param.gen(strategy, num)

    def gen_data_frame(self, strategy, num):
        '''
        Generate data frame containing requested number of rows using specified sampling strategy.
        '''
        data = {param.name: self.gen_param_values(param, strategy, num)
                for param in self.params}
        return pd.DataFrame(data, columns=[param.name for param in self.params])

    def fix_param(self, param, value):
        '''
        Fix model parameter to a constant value, overriding the sampling strategy.
        '''
        self.fixed_params[param] = value

    def unfix_param(self, param):
        '''
        Undo parameter fixing, making it follow the sampling strategy again.
        '''
        del self.fixed_params[param]
