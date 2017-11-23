from distutils.core import setup

setup(
    name='capsicum',
    version='0.0.1',
    description='Lazy Event Risk Assessment Tool',
    author='Masayoshi Mizutani',
    author_email='mizutani@sfc.wide.ad.jp',
    install_requires=['requests'],
    url='https://github.com/m-mizutani/capsicum',
    packages=['capsicum'],
    test_suite='tests'
)
