
## To Get Started

To simply run this, follow the instructions from discussion 4 slides 

Download the dataset
* wget https://www.dropbox.com/scl/fi/namx1n55xzqil4zbkd5sv/PST.zip?rlkey=impcbm2acqmqhurv2oj0xxysx&dl=1
* unzip PST.zip
* wget https://opendata.aminer.cn/dataset/DBLP-Citation-network-V16.zip
* unzip DBLP-Citation-network-V16.zip

Put the unzipped PST directory into data/ and unzipped DBLP dataset into data/PST/

Clone the baseline repository
* git clone https://github.com/THUDM/paper-source-trace.git
* cd paper-source-trace

Install required packages
* pip install -r requirements.txt

You would then pull this repo into the environment
* git clone https://github.com/wzsmith/cs145-pst.git

And you would continue to run any python script by
* python NAME_OF_FILE.py

## chatglm_MV.py

* added chatglm on top of the base code
```
chatgpt_responses = []
  for context in contexts_sorted:
    input_ids = chatgpt_tokenizer.encode(context, return_tensors="pt", max_length=512, truncation=True).to(device)
    output = chatgpt_model.generate(input_ids, max_length=100, num_return_sequences=1, pad_token_id=chatgpt_tokenizer.eos_token_id)
    response = chatgpt_tokenizer.decode(output[0], skip_special_tokens=True)
    chatgpt_responses.append(response)
```
* For each context, generates a response using the GPT-2 model and decodes it. Stores these responses in a list.
```
chatgpt_predictions = [1 if response.startswith("positive") else 0 for response in chatgpt_responses]
```
* Converts the GPT-2 responses into binary predictions: 1 if the response starts with "positive", otherwise 0
```
all_predictions = [chatgpt_predictions, y_score]
final_predictions = majority_vote(all_predictions)
```
* Collects the predictions from both models (GPT-2 and BERT).
* Uses a majority voting mechanism to determine the final predictions.
* majority_vote is a previous function already defined, simply takes an array of values and takes the average, then rounds it up

## logreg.py


