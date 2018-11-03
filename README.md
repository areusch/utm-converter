# UTM track to GPX converter

Converts UTM track files to GPX.

The input UTM file should be a bunch of lines like:

    H4 0272210 4171031 Stream crossing, Trees.

Outputs a GPX file containing one route.

# Running

First install the virtualenv (you need to `pip install pipenv` if you don't
have it):

    $ pipenv install

Then run the tool:

    $ pipenv run convert/convert.py --zone=23N your/utm/file.utm output/gpx.gpx

You can also use it as a filter:

    $ cat utm | pipenv run convert/convert.py --zone=12S
