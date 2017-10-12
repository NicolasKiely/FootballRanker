#!/bin/bash

if [[ -z "$1" ]]; then
  echo "Usage: $0 <week #>"
  exit
fi


python fetch_matches.py 2017
python ranker.py 2017 2016
python picker.py 2017 bb > output/week${1}.txt
python predictor.py 2017 > output/week_${1}_predictions.txt
