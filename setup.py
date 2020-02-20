from setuptools import setup, find_packages

setup(
    name="ATE",
    version="1.0.0",
    author="Graham Van Goffrier",
    packages=find_packages(exclude=['*test']),
    install_requires=['numpy', 'matplotlib', 'pandas', 'docker'],
    # entry_points={
    #    'console_scripts': [
    #        'tbrsample = ATE.command:process'
    #        ]}
)
