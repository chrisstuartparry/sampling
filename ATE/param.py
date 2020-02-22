import pandas as pd


class Parameter:
    '''
    Holds name, acceptable values, (and sampling distribution) for an input parameter.
    '''

    def __init__(self, name, valuerange=[], values=[], sums_to=None, sums_with=[]):
        self.name = name
        if len(values) == 0:
            self.val = valuerange
            self.discrete = False
            self.sums_to = sums_to
            self.sums_with = sums_with
        else:
            self.val = values
            self.discrete = True
            self.sums_to = None
            self.sums_with = []

    def gen(self, strategy, num, parents):
        '''
        Generate requested number of values using the provided sampling strategy.
        '''
        if self.discrete:
            return strategy.gen_discrete(self, num, parents)
        else:
            if self.sums_to is None:
                return strategy.gen_continuous(self, num, parents)
            else:
                parent_records = zip(*[parents[parent.name]
                                       for parent in self.sums_with])
                return [self.sums_to - sum(parent_record) for parent_record in parent_records]

    def transform_columns(self):
        '''
        Get column names for transformed representation.
        '''
        if self.discrete:
            return ['%s_%s' % (self.name, val) for val in self.val]
        else:
            return [self.name]


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
        FWCM = Parameter('firstwall_coolant_material',
                         values=['H2O', 'He', 'D2O'])
        BLT = Parameter('blanket_thickness',
                        valuerange=[0, 500])
        BSM = Parameter('blanket_structural_material',
                        values=['SiC', 'eurofer'])
        BBM = Parameter('blanket_breeder_material',
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
        BCF = Parameter('blanket_coolant_fraction',
                        valuerange=[0, 1],
                        sums_to=1,
                        sums_with=[BMF, BBF, BSF])

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

    def gen_param_values(self, param, strategy, num, parents):
        '''
        Generate requested number of values for a single parameter using specified sampling strategy.
        '''
        if param.name in self.fixed_params:
            return self.fixed_params[param.name]
        else:
            return param.gen(strategy, num, parents)

    def gen_data_frame(self, strategy, num):
        '''
        Generate data frame containing requested number of rows using specified sampling strategy.
        '''
        data = {param.name: self.gen_param_values(param, strategy, num, {})
                for param in self.params if param.sums_to is None}
        data.update({param.name: self.gen_param_values(param, strategy, num, data)
                     for param in self.params if param.sums_to is not None})
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
