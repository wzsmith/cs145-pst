import json


def avg_precision(validate_json_filepath, submission_json_filepath, annotated_result_filepath):
    """
    Initial Goal: Calculate Mean Average Precision
     
    Average Precision: AP(v_q( = (1/r_q) * sum_{k=1}^{M} P_q(k) * 1_k
    Mean Average Precision: MAP = (1/n) * sum_{q=1}^(n} AP(v_q)

    validate_json and submission_json are json files
    annotated_result is a txt filei

    We look for each referred paper in the validate json, then find the average
    of its values in the submission_data floats
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
        M, reference_list = len(paper["references"]), paper["references"]
        r_q = annotated_file_data[:M].count("1")
        precision_result_sum = 0
        # print(paper["_id"], M, len(submission_data[paper["_id"]]))
        tp = 0
        fp = 0
        for i in range(M):
            try:
                referred_paper = reference_list[i]
                if referred_paper in submission_data:
                    avg_weight = sum(submission_data[referred_paper]) / len(submission_data[referred_paper])
                    if avg_weight >= 0.5:
                        # Then its positive
                        # Now we check against real result
                        if int(annotated_file_data[0]) == 1:
                            # Then true positive
                            tp += 1
                        else:
                            # Then false positive
                            fp += 1
                    precision = tp / (tp + fp)
                    precision_result_sum += precision * int(annotated_file_data[0])
                annotated_file_data.pop(0)
            except:
                continue
        avg_precision_list.append(precision_result_sum / (r_q + 1e-5))
    return avg_precision_list

def mean_avg_precision(avg_precision_list):
    return sum(avg_precision_list) / len(avg_precision_list)

# We found that the above approach for calculating an average precision metric was difficult. 
# There was a discrepancy in the files provided
# The above functions returns a value of 0 when we knew what we were supposed to return was not 0
# It was clear that the approach we took with via the averages was not useful
# It appeared that the XML files located in the directory were being used to generate the submission file once the bert.py
# file was run as the baseline. As such, we did the following instead:

def influential_papers(validate_json_filepath, submission_json_filepath):
    """
    1. Get the list of referred papers from the paper_source_trace json file
    2. Go through each paper and see if that paper has a corresponding entry in the submission json
    3. Find the average value present in the submission json entry for that paper; larger values represent more influence
    4. Compile a list describing the papers with the most influential references from greatest to least
    """

    with open(validate_json_filepath, "r") as r_validate:
        validation_data = json.load(r_validate)
    with open(submission_json_filepath, "r") as r_submission:
        submission_data = json.load(r_submission)    
    paper_influence_dict = {}
        
    for paper in validation_data:
        M, reference_list = len(paper["references"]), paper["references"]
        paper_influence = 0
        for i in range(M):
            try:
                referred_paper = reference_list[i]
                if referred_paper in submission_data:
                    avg_weight = sum(submission_data[referred_paper]) / len(submission_data[referred_paper])
                    paper_influence += avg_weight
            except:
                continue
        paper_influence_dict[paper["_id"]] = paper_influence
    
    for paper in list(paper_influence_dict):
        if paper_influence_dict[paper] == 0:
            del paper_influence_dict[paper]
    paper_influence_dict = sorted(paper_influence_dict.items(), key=lambda item: item[1], reverse=True)
    return paper_influence_dict

if __name__ == "__main__":
    # Change filepaths to proper locations when running locally
    validate_json_filepath = "/Users/ssreenivasan/cs145-pst/data/PST/paper_source_trace_valid_wo_ans.json"
    submission_json_filepath = "/Users/ssreenivasan/cs145-pst/data/PST/valid_submission_scibert.json"
    annotated_result_filepath = "/Users/ssreenivasan/cs145-pst/data/PST/bib_context_valid_label.txt"

    avg_prec_list = avg_precision(validate_json_filepath, submission_json_filepath, annotated_result_filepath)
    print(f"The mean average precision is: {mean_avg_precision(avg_prec_list)}")

    print(f"The most influential papers are:
          {influential_papers(validate_json_filepath, submission_json_filepath)}")

