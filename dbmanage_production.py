#!/usr/bin/env python
from migrate.versioning.shell import main

main(url='sqlite:///production.db',repository='db_repo')
