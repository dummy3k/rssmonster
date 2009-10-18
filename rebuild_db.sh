#!/bin/bash

rm -rf data/
rm development.db
./dbmanage_dev.py version_control
./dbmanage_dev.py upgrade

