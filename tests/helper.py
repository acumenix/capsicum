import yaml
import os

DEFAULT_TEST_CONFIG = './test.yml'
TEST_CONFIG_PATH = (os.environ.get('CAPSICUM_TEST_CONFIG') or
                    DEFAULT_TEST_CONFIG)
if os.path.exists(TEST_CONFIG_PATH):
    TEST_PREF = yaml.load(open(TEST_CONFIG_PATH, 'rt'))
else:
    TEST_PREF = None
