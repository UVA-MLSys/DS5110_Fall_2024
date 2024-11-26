from setuptools import setup, find_packages

setup(
    name='cosmicai',
    # packages=["Team 4"],
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    version='0.0.1',
    url='https://github.com/UVA-MLSys/DS5110_Fall_2024',
    author='Ryan Healy',
    author_email='rah5ff@virginia.edu',
    description='Scaling Redshift Predictions',
    license='MIT',
)