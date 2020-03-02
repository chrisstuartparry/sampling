import pandas as pd

from .param import Parameter, ContinuousParameter, DiscreteParameter, SumParameterGroup


class Domain:
    '''
    Holds all parameters of the model.
    '''

    def __init__(self):
        '''
        Generates array of input parameters for model in use.
        '''
        FWT = ContinuousParameter('firstwall_thickness', 'FW thickness', 0, 20)
        FWAM = DiscreteParameter(
            'firstwall_armour_material', 'FW armour', ['tungsten'])
        FWSM = DiscreteParameter(
            'firstwall_structural_material', 'FW structure', ['SiC', 'eurofer'])
        FWCM = DiscreteParameter(
            'firstwall_coolant_material', 'FW coolant', ['H2O', 'He', 'D2O'])
        BLT = ContinuousParameter(
            'blanket_thickness', 'Blanket thickness', 0, 500)
        BSM = DiscreteParameter('blanket_structural_material',
                                'Blanket structure', ['SiC', 'eurofer'])
        BBM = DiscreteParameter('blanket_breeder_material', 'Blanket breeder', [
                                'Li4SiO4', 'Li2TiO3'])
        BMM = DiscreteParameter(
            'blanket_multiplier_material', 'Blanket multiplier', ['Be', 'Be12Ti'])
        BCM = DiscreteParameter(
            'blanket_coolant_material', 'Blanket coolant', ['H2O', 'He', 'D2O'])
        BBEF = ContinuousParameter(
            'blanket_breeder_li6_enrichment_fraction', 'Blanket breeder Li6 enrichment', 0, 1)
        BBPF = ContinuousParameter(
            'blanket_breeder_packing_fraction', 'Blanket breeder packing', 0, 1)
        BMPF = ContinuousParameter(
            'blanket_multiplier_packing_fraction', 'Blanket multiplier packing', 0, 1)
        BFS = SumParameterGroup('blanket_fractions', 'Blanket fractions', [('blanket_multiplier_fraction', 'Blanket multiplier %'),
                                                                           ('blanket_breeder_fraction',
                                                                            'Blanket breeder %'),
                                                                           ('blanket_structural_fraction',
                                                                            'Blanket structure %'),
                                                                           ('blanket_coolant_fraction',
                                                                            'Blanket coolant %')
                                                                           ], 1)

        FWFS = SumParameterGroup('firstwall_fractions', 'FW fractions', [('firstwall_armour_fraction', 'FW armour %'),
                                                                         ('firstwall_structural_fraction',
                                                                          'FW structure %'),
                                                                         ('firstwall_coolant_fraction',
                                                                          'FW coolant %')
                                                                         ], 1)

        self.params = [FWT, FWAM, FWSM, FWCM, BLT, BSM, BBM,
                       BMM, BCM, BBEF, BBPF, BMPF, BFS, FWFS]
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
        data = {}
        for param in self.params:
            data.update(self.gen_param_values(param, strategy, num))

        return pd.DataFrame(data)

    def fix_param(self, param, value):
        '''
        Fix model parameter to a constant value, overriding the sampling strategy.
        '''
        self.fixed_params[param.name] = param.fix(value)

    def unfix_param(self, param):
        '''
        Undo parameter fixing, making it follow the sampling strategy again.
        '''
        del self.fixed_params[param]
