import os
import json
import numpy as np

# Apply ensemble methods to the predictions of the models to hopefully achieve a better result

# IMPORTANT: The jsons in input must be formatted in the way: name_{5 digit accruacy no decimal}.json}
# Ex. Submission_34387.json = 34.387% accuracy
"""
Loads all of the jsons in the given directory in the approriate format

returns: A list of the jsons loaded (dict: key = filename, value = [accuracy, data])
"""
def load_data(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                data[filename] = {"accuracy": float(filename[:-5][-5:]) / 1000, "data": json.load(file)}
                # print(float(filename[:-5][-5:]) / 1000)
    return data

"""
Applies the appropriate ensemble method to the inputted data
data: A list of the jsons loaded (dict: key = filename, value = [accuracy, data])
method: can be any of the following: mean, median, moe
(moe = "mixture of experts")

returns: The ensemble method applied to the data
"""
def apply_ensemble_methods(data, method="mean"):
    predictions = [data[filename]["data"] for filename in data]

    result = {}

    # Every output should have the same length so we can just use the first one to find lengths
    for id in predictions[0]: # For every ID
        result[id] = [0] * len(predictions[0][id]) 
        for i in range(len(predictions[0][id])): # For each score in that ID

            # Get the scores from every prediction for that specific score
            scores = [predictions[j][id][i] for j in range(len(predictions))]

            # Apply ensemble methods
            # Mean
            if method == "mean":
                result[id][i] = np.mean(scores)

            # Median
            if method == "median":
                result[id][i] = np.median(scores)

            # Mixture of experts
            if method == "moe":
                # Weights for each model
                accuracies = np.array([data[filename]["accuracy"] for filename in data])
                accuracies = accuracies / np.sum(accuracies) # Normalize the weights

                # Apply the weights
                result[id][i] = np.dot(scores, accuracies)

    if len(result) == 0:
        print("ERROR: Ensemble Method not found")
        return None
    
    return result

if __name__ == "__main__":
    predictions = load_data(os.getcwd() + "/inputs")
    result = apply_ensemble_methods(predictions, "mean")
    with open("outputs/ensemble.json", 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    