In order to get ensemble.py to work there's several setup instructions:

1. Make two folders called "inputs" and "outputs"
2. Drag all of your kddcup json submissions into "inputs"
3. For all of the jsons in submissions, modify it such that the last 5 digits of the file name
contains the digits of the accuracy score online (ex. 0.34387 on website = 34387)
- Filename example: "valid_submission_scibert_34387.json"
4. In ensemble.py in the main method, change the "method" parameter to the appropriate online
- Options are: mean, median, moe
5. Run "python ensemble.py" and your output file should be in your outputs folder