from ATE import UniformSamplingStrategy, Domain
import numpy as np


def generate_params_fix_disc():
    n_batches = 100
    n_samples_per_batch = 1000
    seed = 2

    print('Seed is %d' % seed)
    print('Each batch will contain %d samples' % n_samples_per_batch)

    np.random.seed(seed)

    domain = Domain()
    sampling_strategy = UniformSamplingStrategy()

    discrete_params = [
        {
            'firstwall_armour_material': 'tungsten',
            'firstwall_structural_material': 'eurofer',
            'firstwall_coolant_material': 'H2O',
            'blanket_coolant_material': 'H2O',
            'blanket_multiplier_material': 'Be12Ti',
            'blanket_breeder_material': 'Li4SiO4',
            'blanket_structural_material': 'eurofer',
        },
        {
            'firstwall_armour_material': 'tungsten',
            'firstwall_structural_material': 'eurofer',
            'firstwall_coolant_material': 'H2O',
            'blanket_coolant_material': 'He',
            'blanket_multiplier_material': 'Be12Ti',
            'blanket_breeder_material': 'Li4SiO4',
            'blanket_structural_material': 'eurofer',
        },
        {
            'firstwall_armour_material': 'tungsten',
            'firstwall_structural_material': 'eurofer',
            'firstwall_coolant_material': 'He',
            'blanket_coolant_material': 'H2O',
            'blanket_multiplier_material': 'Be12Ti',
            'blanket_breeder_material': 'Li4SiO4',
            'blanket_structural_material': 'eurofer',
        },
        {
            'firstwall_armour_material': 'tungsten',
            'firstwall_structural_material': 'eurofer',
            'firstwall_coolant_material': 'He',
            'blanket_coolant_material': 'He',
            'blanket_multiplier_material': 'Be12Ti',
            'blanket_breeder_material': 'Li4SiO4',
            'blanket_structural_material': 'eurofer',
        }
    ]

    df = domain.gen_data_frame(
        sampling_strategy, n_batches * n_samples_per_batch)

    save_idx = 0

    for param_set in discrete_params:
        for param, param_value in param_set.items():
            df[param] = param_value

        for batch_idx in range(n_batches):
            offset = batch_idx * n_samples_per_batch
            subdf = df.iloc[offset:(offset+n_samples_per_batch)]
            subdf.to_csv('output/run2/batch%d_in.csv' % save_idx, index=False)

            if save_idx % 10 == 0:
                print('Generated batch %d of %d' %
                      (save_idx + 1, len(discrete_params) * n_batches))

            save_idx += 1


if __name__ == '__main__':
    generate_params_fix_disc()
