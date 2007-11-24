#!/usr/bin/env python

from os.path import join

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('stats', parent_package, top_path, setup_name = 'setupscons.py')

    config.add_subpackage('models')
    config.add_data_dir('tests')

    config.add_sconscript('SConstruct')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
