#!/bin/bash

rm test.db

coverage run -m pytest --disable-warnings -q

coverage report

