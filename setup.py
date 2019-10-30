import os
from setuptools import setup, find_packages


basedir = os.path.dirname(__file__)
with open(os.path.join(basedir, 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()


setup(
    name='stretched-wire',
    version=__version__,
    description="LNLS magnet's group stretched wire control package",
    url='https://github.com/lnls-ima/stretched-wire',
    author='lnls-ima',
    license='GNU License',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'pyqtgraph',
        'qtpy',
    ],
    package_data={'stretched-wire': ['VERSION']},
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False,
)
