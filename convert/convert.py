import argparse
import collections
import re
import sys

from gpxpy import gpx
import utm


DESCRIPTION = """\
Convert Garmin (?) route files containing UTM coordinates to GPX.
"""


Zone = collections.namedtuple('Zone', 'number letter')


def _Zone(x):
  m = re.match(r'([0-9]{1,2})([A-Z])', x)
  if not m:
    raise argparse.ArgumentTypeError(
        'Malformed zone (want <number><letter> i.e. 11N)')
  number = int(m.group(1))
  if number > 60:
    raise argparse.ArgumentTypeError('Zone number out of range [1,60]')

  letter = m.group(2)
  if letter not in utm.conversion.ZONE_LETTERS:
    raise argparse.ArgumentTypeError(
        'Zone letter must be one of %s' % utm.conversion.ZONE_LETTERS)

  return Zone(number, letter)


def _ParseArgs(argv):
  parser = argparse.ArgumentParser(description=DESCRIPTION, prog=argv[0])
  parser.add_argument('--zone',
                      required=True,
                      type=_Zone,
                      help='UTM zone # and letter (i.e. 11S)')
  parser.add_argument('utm_file', nargs='?', help='UTM GPS file')
  parser.add_argument('gpx_file', nargs='?', help='GPX file')

  return parser.parse_args(argv[1:])


class MalformedLineException(Exception):
  """Raised when UTM input data not recognized."""


UTM_RE = re.compile(
    r'^(?P<id>[^ ]+) (?P<easting>[0-9]+) (?P<northing>[0-9]+) '
    r'(?P<description>.*)$')


def Convert(utm_file, gpx_file, zone):
  gpx_obj = gpx.GPX()
  route = gpx.GPXRoute(name='UTM route')
  gpx_obj.routes.append(route)

  for line in utm_file:
    m = UTM_RE.match(line[:-1])  # strip trailing \n
    if not m:
      raise MalformedLineException(line)

    lat, lng = utm.to_latlon(int(m.group('easting')), int(m.group('northing')),
                             zone.number, zone.letter)
    route.points.append(gpx.GPXRoutePoint(
        lat, lng, name=m.group('id'), description=m.group('description')))

  gpx_file.write(gpx_obj.to_xml())
  gpx_file.write('\n')  # terminating newline not written by default


def Main(argv):
  args = _ParseArgs(argv)

  utm_file = None
  if args.utm_file:
    utm_file = open(args.utm_file)
  else:
    utm_file = sys.stdin
    
  gpx_file = None
  if args.gpx_file:
    gpx_file = open(args.gpx_file, 'w')
  else:
    gpx_file = sys.stdout

  Convert(utm_file, gpx_file, zone=args.zone)


if __name__ == '__main__':
  Main(sys.argv)
