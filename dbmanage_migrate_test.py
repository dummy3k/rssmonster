#!/usr/bin/env python
from migrate.versioning.shell import main

main(url='sqlite:///migrate_test.db',repository='db_repo')
