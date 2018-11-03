import os
import os.path
import tempfile

import pytest
from . import convert

def test_convert(utm):
  gpx = '%s.gpx' % os.path.splitext(utm)[0]
  
  # UTM files should be named case_zone.utm
  zone = os.path.splitext(utm)[0].rsplit('_', 1)[1]
  with tempfile.NamedTemporaryFile() as tmp:
    convert.Main(['convert', '--zone', zone, utm, tmp.name])

    with open(tmp.name) as tmp_read:
      actual = tmp_read.read()

    with open(gpx) as gpx_read:
      expected = gpx_read.read()

    assert actual == expected

  
