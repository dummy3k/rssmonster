#!/bin/bash

rm -rf data/
rm development.db
rm db_repo/versions/*.py~
rm db_repo/versions/*.pyc

./dbmanage_dev.py version_control
./dbmanage_dev.py upgrade

