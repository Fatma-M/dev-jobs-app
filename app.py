from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# CREATE ROUTE FOR DATA TO USE IN JS CODE
@app.route('/get_data', methods=['GET'])
def get_csv_data():
    data = []
    with open('./static/data.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
            
    return data

# CREATE HOME ROUTE WITH index.html
@app.route("/")
def home_page():
    return render_template("index.html")

# CREATE ADD JOB JOB ROUTE
@app.route("/add-job")
def add_job_page():
    return render_template("add-job.html")

# CREATE JOB DETAILS ROUTE
@app.route("/job-details/<id>", methods=['GET'])
def job_details_page(id):
    data_source = get_csv_data()
    item = None

    for entry in data_source:
        if entry['id'] == id:
            item = entry
            break

# EXTRACT JOB DATA
    if item is not None:
        logo = item["logo"]
        logo_background = item["logoBackground"]
        company = item["company"]
        position = item["position"]
        postedAt = item["postedAt"]
        contract = item["contract"]
        location = item["location"]
        website = item["website"]
        apply = item["apply"]
        description = item["description"]
        requirements_content = item["requirements/content"]
        role_content = item["role/content"]
        # Retrieve the requirements items and role items
        requirements_items = [item.get(f"requirements/items/{i}") for i in range(7)]
        role_items = [item.get(f"role/items/{i}") for i in range(5)]
        # Check if any of the requirements and role items are empty
        non_empty_requirements_items = [req for req in requirements_items if req and req.strip()]
        non_empty_role_items = [role for role in role_items if role and role.strip()]

        return render_template("job-details.html", logo=logo, logo_background=logo_background, company=company, position=position, postedAt=postedAt, contract=contract, location=location, website=website, apply=apply, description=description, requirements_content=requirements_content, requirements_items=non_empty_requirements_items, role_content=role_content, role_items=non_empty_role_items)
    
    else:
        return "Data not found"


# RUN APP WITH DEBUG MODE
if __name__ == '__main__':
    app.run(debug=True)
