#!/bin/bash

days=("Monday")

for day in "${days[@]}"; do
  python3 gendriver.py 20 boring nova male openai $day
done