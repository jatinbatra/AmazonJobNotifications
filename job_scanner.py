name: Verbose Job Check

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
        run: |
          python -m pip install --upgrade pip
          pip install requests
          
      - name: Show Python version
        run: |
          python --version
          pip list
          
      - name: Run check with output
        run: |
          echo "Starting job check..."
          python -u test.py
          echo "Job check completed."
