name: Job Check

on:
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          
      - name: Install requests
        run: pip install requests
        
      - name: Run check
        run: python test.py
