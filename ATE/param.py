import pandas as pd


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

    def gen(self, strategy, num):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        if self.discrete:
            return strategy.gen_discrete(self, num)
        else:
            return strategy.gen_continuous(self, num)


class Domain:
    '''
    Holds all parameters of the model.
    '''

    def __init__(self):
        '''
        Generates array of input parameters for model in use.
        '''
        FWT = Parameter('firstwall_thickness',
                        valuerange=[0, 20])
        FWAM = Parameter('firstwall_amour_material',
                         values=['tungsten'])
        FWSM = Parameter('firstwall_structural_material',
                         values=['SiC', 'eurofer'])
        FWCM = Parameter('firstwall_coolant_material]',
                         values=['H2O', 'He', 'D2O'])
        BSM = Parameter('blanket_structural_material',
                        values=['SiC', 'eurofer'])
        BBM = Parameter('blanket_breeder_material ',
                        values=['Li4SiO4', 'Li2TiO3'])
        BMM = Parameter('blanket_multiplier_material',
                        values=['Be', 'Be12Ti'])
        BCM = Parameter('blanket_coolant_material',
                        values=['H2O', 'He', 'D2O'])
        BBEF = Parameter(
            'blanket_breeder_li6_enrichment_fraction', valuerange=[0, 1])
        BBPF = Parameter('blanket_breeder_packing_fraction',
                         valuerange=[0, 1])
        BMPF = Parameter('blanket_multiplier_packing_fraction',
                         valuerange=[0, 1])
        BMF = Parameter('blanket_multiplier_fraction',
                        valuerange=[0, 1])
        BBF = Parameter('blanket_breeder_fraction',
                        valuerange=[0, 1])
        BSF = Parameter('blanket_structural_fraction',
                        valuerange=[0, 1])
        # BCF = 1 - BMF - BBF - BSF (blanket_coolant_fraction)

        self.params = [FWT, FWAM, FWSM, FWCM, BSM, BBM,
                       BMM, BCM, BBEF, BBPF, BMPF, BMF, BBF, BSF]
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
