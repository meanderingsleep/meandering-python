#!/bin/bash

days=("Saturday" "Sunday")

for day in "${days[@]}"; do
  python3 gendriver.py 20 boring onyx male openai $day
  python3 gendriver.py 20 boring nova female openai $day
  python3 gendriver.py 20 meandering onyx male openai $day
  python3 gendriver.py 20 meandering nova female openai $day
done