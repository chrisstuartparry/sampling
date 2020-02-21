from setuptools import setup, find_packages

setup(
    name='ATE',
    version='1.0.0',
    author='Graham Van Goffrier, Petr Mánek',
    packages=find_packages(exclude=['*tests']),
    install_requires=['numpy', 'matplotlib',
                      'pandas', 'docker', 'scikit-learn'],
    # entry_points={
    #    'console_scripts': [
    #        'tbrsample = ATE.command:process'
    #        ]}
)
