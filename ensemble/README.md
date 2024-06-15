# Ensemble Folder Instructions

(Same as in the main repository `README.md`)

In order to get ensemble.py to work there's several setup instructions:

1. Make two folders called "inputs" and "outputs"
2. Drag all of your kddcup json submissions into "inputs"
3. For all of the jsons in submissions, modify it such that the last 5 digits of the file name
contains the digits of the accuracy score online (ex. 0.34387 score = 34387)
- Filename example: "valid_submission_scibert_34387.json"
4. In ensemble.py in the main method, change the "method" parameter to the appropriate option
- Options are: mean, median, wmean
5. Run "python ensemble.py" and your output file should be in your outputs folder

(Note: "wmean" = weighted average)

For the purpose of this folder we provided the 4 inputs used when ensembling our final result.

If you dont want a specific file to be used in the ensemble you can simply place it into the outputs folder or somewhere else outside of the inputs folder.