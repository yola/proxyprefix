"""Configuration for testtube.

Automatically run tests when files change by running: stir

See: https://github.com/thomasw/testtube

"""
from testtube.helpers import Helper, Nosetests, Flake8


class Clear(Helper):
    command = 'clear'


clear = Clear(all_files=True)
lint = Flake8(all_files=True)
test = Nosetests()

PATTERNS = (
    (r'.*\.py$', [clear, lint], {'fail_fast': True}),
    (r'(.*setup\.cfg$)|(.*\.py$)', [test]),
)
