# cs145-pst

UCLA CS145: Introduction to Data Mining
Final Project: 2024 KDD-Cup PST Submission
Team: CS145 Data Miners
Tyler Tran, Roland Yang, Henry Liu, Aaron Chien, William Smith, Sreejeet Sreenivasan

## Prerequisites
- Linux
- Python 3.9
- PyTorch 1.10.0+cu111

## Getting Started

Video Presentation Link:
https://www.youtube.com/watch?v=hdaPMrQ4l_Q&ab_channel=whyroland

Presentation Slides:
https://docs.google.com/presentation/d/1XTWjGr-PaRbw-ZiRx-aJ2kl-hdAnEY7Hb70ba-o2hu0/edit?usp=sharing

Report Paper:
https://drive.google.com/file/d/1W5gOWutFrJJSFvq2idvjhc6ao94s0f2H/view?usp=sharing

The instructions below will walk you through with reproducing an output near accurate to our final submission output (our actual final submission that achieved a score of ~0.37687 can be found in this folder as `final_submission.json`)

## Setup (Datasets and Installation)

Before proceeding, make sure to download the appropriate datasets. Create a folder called "data" in the repository and then download all the required datasets. The following bash commands below may help.

We utilize the provided public PST dataset provided by the competition organizers and the 

```bash
# Make data directory in root folder and navigate into it
mkdir data
cd data

# Download the PST dataset
wget https://www.dropbox.com/scl/fi/namx1n55xzqil4zbkd5sv/PST.zip?rlkey=impcbm2acqmqhurv2oj0xxysx&dl=1
unzip PST.zip # May be a different name than "PST.zip"

# Download the DBLP Citation Network
wget https://opendata.aminer.cn/dataset/DBLP-Citation-network-V16.zip
unzip DBLP-Citation-network-V16.zip
```

Put the unzipped PST folder into `data/` and the DBLP dataset into `data/PST`

After downloading and setting up the datasets- make sure you have all necessary dependencies installed. If at any point you come across a missing package error in running any of the scripts just `pip install` it.
```
pip install -r requirements.txt
```

## Training

We need to train 4 different SciBERT models and then properly ensemble their results using `ensemble.py` in `ensemble/`.

```bash
# Train SciBERT model
python bert.py
# output at out/kddcup/scibert/
```

The output can be found in `out/kddcup/scibert` under the name of `valid_submission_scibert.json`. Following this run an evaluation on the outputted json by whatever methodology you choose to obtain a MAP score. We did so by submitting it online.

Rename the file such that the last 5 characters before the file extension "json" contain the digits pertaining to your MAP score.

(Ex. 0.34387 score = 34387, filename would be "valid_submission_scibert_34387.json")

Move the renamed file containing the predictions into `ensemble/inputs/`

Repeat the aformentioned training steps explained above 4 times (or however many times you decide to choose, 4 was just our experimental optimal value).

## Ensembling

You should now have 4 jsons inside of `ensemble/inputs/` containing renamed prediction files using the file naming convention explained above. (Feel free to refer to the `README.md` inside the `ensemble/` folder for the same instructions below)

If you haven't done so yet, create a directory called `outputs` inside of `ensemble/`.

In `ensemble.py` in the main method, change the `method` parameter to the appropriate option. To reproduce our results set it to `"wmean"`

```python
# ... Below is Lines 30/31
def apply_ensemble_methods(data, method="wmean"): # method parameter
    predictions = [data[filename]["data"] for filename in data]
# ...
```

Execute the script and your final output should be in `ensemble/outputs/` under the name `ensemble.json`.

```bash
# Ensemble all of the predictions
python ensemble.py
# output at ensemble/outputs/
```

(Note: we provided the 4 original prediction jsons that we ensembled for our final submission in the folder)

## Explanation of Other Files

All work relevant to the project report

### Aaron's Folder

The folder with the name `Aaron` contains all of Aaron's code contributions to the project. Opening the folder and accessing the `README.md` in that folder specifically will provide you with further information on all of his code and how to execute it

### Notebooks

There are two notebooks in this repository.

`Chain_Of_Thought.ipynb` contains our attempt at using Chain of Thought with LLMs to make a PST model. You can run it by following the instructions below.

1. Open Chain_Of_Thought.ipynb
2. Run all of the cells

`PST_Data_Trend_Visualizations.ipynb` contains code used to create the visualizations shown in the project report. You can run it by using the instructions below.

1. Open PST_Data_Trend_Visualizations.ipynb
2. Run all of the cells

### evaluate.py

Our algorithm for finding the MAP score offline.

Inside of `evaluate.py` change the filepaths inside of the main method at the bottom to the appropriate locations.

```python
# Change filepaths to proper locations when running locally (Line 107)
validate_json_filepath = ".../paper_source_trace_valid_wo_ans.json"
submission_json_filepath = ".../valid_submission_scibert.json"
annotated_result_filepath = ".../bib_context_valid_label.txt"
```

After that execute the file. Output should be similar to `influentialPapers.json` in this repository.

```bash
python evaluate.py
```
