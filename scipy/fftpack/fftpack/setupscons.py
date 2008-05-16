#!/usr/bin/env python
# Created by Pearu Peterson, August 2002

from os.path import join

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('fftpack',parent_package, top_path)

    config.add_sconscript("SConstruct")

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
