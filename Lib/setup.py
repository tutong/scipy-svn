
def configuration(parent_package='',top_path=None):
    from scipy.distutils.misc_util import Configuration
    config = Configuration('scipy',parent_package,top_path)
    #config.add_subpackage('sandbox')
    config.add_subpackage('utils')
    config.add_subpackage('io')
    config.add_subpackage('special')
    config.add_subpackage('optimize')
    config.add_subpackage('stats')
    config.add_subpackage('interpolate')
    config.make_svn_version_py()  # installs __svn_version__.py
    return config

if __name__ == '__main__':
    from scipy.distutils.core import setup
    setup(**configuration(top_path='').todict())
