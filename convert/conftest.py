import glob
import os
import os.path

def pytest_addoption(parser):
  parser.addoption('--utm', action='append', default=[],
                   help='utm file to test')


def pytest_generate_tests(metafunc):
  utms = metafunc.config.getoption('utm')
  if utms:
    metafunc.parametrize('utm', utms)
  else:
    testdata_dir = os.path.join(os.path.dirname(__file__), 'testdata')
    metafunc.parametrize('utm', glob.glob('%s/*.utm' % testdata_dir))


