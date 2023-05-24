#!/bin/sh
cd app/data
curl -sO "https://s3.amazonaws.com/tripdata/2022{01,02,03,04,05,08,09,10,11,12}-citibike-tripdata.csv.zip"
curl -sO "https://s3.amazonaws.com/tripdata/2022[06-07]-citbike-tripdata.csv.zip"
unzip -q "*.csv.zip" -x "__MACOSX/*"
cd ../..
