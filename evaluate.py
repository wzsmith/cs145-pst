import json

def avg_precision(validate_json_filepath, submission_json_filepath, annotated_result_filepath):
    """
    validate_json and submission_json are json files
    annotated_result is a txt file
    """
    with open(validate_json_filepath, "r") as r_validate:
        validation_data = json.load(r_validate)
    with open(submission_json_filepath, "r") as r_submission:
        submission_data = json.load(r_submission)    
    avg_precision_list = []
    
    # Read in txt file into the list of 0s and 1s that are in annotated_result
    with open(annotated_result_filepath, "r") as annotated_file:
        annotated_file_data = annotated_file.read().split("\n")
    
    for paper in validation_data:
        M = len(paper["references"])
        # M = len(submission_data[paper["_id"]])
        r_q = annotated_file_data[:M].count("1")
        precision_result_sum = 0
        # print(paper["_id"], M, len(submission_data[paper["_id"]]))
        tp = 0
        fp = 0
        for i in range(M):
            try:
                val = submission_data[paper["_id"]][i]
                if float(val) >= 0.5:
                    # Then this val is a positive example
                    if int(annotated_file_data[0]) == 1:
                        tp += 1
                    elif int(annotated_file_data[0]) == 0:
                        fp += 1
                precision = tp / (tp + fp)
                precision_result_sum += precision * int(annotated_file_data[i])
                annotated_file_data.pop(0)
            except:
                continue
        avg_precision_list.append(precision_result_sum / (r_q + 1e-5))

    return avg_precision_list

def mean_avg_precision(avg_precision_list):
    return sum(avg_precision_list) / len(avg_precision_list)

if __name__ == "__main__":
    # Change filepaths to proper locations when running locally
    validate_json_filepath = "/Users/ssreenivasan/cs145-pst/data/PST/paper_source_trace_valid_wo_ans.json"
    submission_json_filepath = "/Users/ssreenivasan/cs145-pst/data/PST/valid_submission_scibert.json"
    annotated_result_filepath = "/Users/ssreenivasan/cs145-pst/data/PST/bib_context_valid_label.txt"

    avg_prec_list = avg_precision(validate_json_filepath, submission_json_filepath, annotated_result_filepath)
    print(mean_avg_precision(avg_prec_list))

