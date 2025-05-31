import ocr
import llama
import re
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

def scan_in_bill(filename):
    match = None
    while match == None:
        text = ocr.recognizecharacters(filename)
        print("Here")
        modeloutputs = llama.askLlamaImg(system='You are an expert at extracting structured data from receipts. Extract a broad description, amount spent, and date from the recipt you are given. First, write out your thought process, then display the data in the format: {"Description":description, "Spent":spent, "Date":"mm/dd/yyyy"}. Do NOT reference this template in your response! Keep the JSON in a single line please', image_path=filename)
        print(modeloutputs)

        # Regex pattern to extract all entries
        pattern = r'\{"Description":\s*"(.*?)",\s*"Spent":\s*(\d+\.\d{2}),\s*"Date":\s*"(.*?)"\}'

        match = re.search(pattern, modeloutputs)
    description, spent, date = match.groups()

    return description, spent, date

def createlabels(bills, max_attempts=5):
    descriptions = [bill[0] for bill in bills]
    for attempt in range(max_attempts):
        modeloutputs = llama.askLlama(
            system='You are an LLM made to categorize receipts. To do this, you are given a list of brief descriptions of the receipt. You are to then categorize them into no more than 10 categories. First, write out your thought process, then display the labels in the format: [1:"label", 2:"label", 3:"label"]. Do NOT reference this template in your response, and do NOT use quotes anywhere else in your answer! Make sure each category is no more than one word long',
            user=str(descriptions)
        )

        print(f"Attempt {attempt+1} output:\n{modeloutputs}")

        pattern = r'\d+:"([^"]+)"'
        labels = re.findall(pattern, modeloutputs)

        # Simple validity check: list length and non-empty strings
        if labels and len(labels) <= 10 and all(label.strip() for label in labels):
            return labels

    raise ValueError("Failed to get valid labels after multiple attempts.")

def categorize(description, categories, max_attempts=5):
    for attempt in range(max_attempts):
        modeloutputs = llama.askLlama(
            system=(
                f'Categorize the following receipt description into one of the following categories: {categories}. '
                'Write your thinking process, then use the form: category:"categoryname". '
                'These labels are case sensitive, so make sure they fit exactly. Select one category from those provided'
            ),
            user=description
        )

        print(f"Attempt {attempt + 1} output:\n{modeloutputs}")

        # Extract category from model output
        pattern = r'category:"([A-Za-z0-9 _-]+)"'
        labels = re.findall(pattern, modeloutputs)

        # Validate label
        if len(labels) == 1 and labels[0] in categories:
            return labels[0]

    raise ValueError("Failed to get a valid category after multiple attempts.")

def produce_graphs(files):
    billinfo = []
    for file in files:
        billinfo.append(scan_in_bill(file))
    
    labels = createlabels(billinfo)

    piedata = {}
    for bill in billinfo:
        description = bill[0]
        spent = bill[1]
        date = bill[2]

        category = categorize(description, labels)  # Extract the first (and only) label
        if category not in piedata:
            piedata[category] = float(spent)
        else:
            piedata[category] += float(spent)

    weekly_expenses = defaultdict(float)

    for bill in billinfo:
        description = bill[0]
        spent = float(bill[1])
        date = datetime.strptime(bill[2], "%m/%d/%Y")
        year_week = date.isocalendar()[:2]  # (year, week number)
        weekly_expenses[year_week] += spent

    # Sort the weeks chronologically
    sorted_weeks = sorted(weekly_expenses.keys())
    totals = [weekly_expenses[week] for week in sorted_weeks]
    labels = [f"Week {week[1]} ({week[0]})" for week in sorted_weeks]

    return ({"labels":list(piedata.keys()), "data":list(piedata.values())},{"weeks": labels, "data":totals}, sum(list(piedata.values())))

if __name__ == "__main__":

    print(produce_graphs(["bill1.jpeg", "bill2.jpeg"]))