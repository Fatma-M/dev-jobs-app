from flask import Flask, render_template, request, redirect
import csv
import uuid

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
        # requirements and role items
        requirements_items = [item.get(f"requirements/items/{i}") for i in range(7)]
        role_items = [item.get(f"role/items/{i}") for i in range(5)]
        # Check if any of the requirements and role items are empty
        non_empty_requirements_items = [req for req in requirements_items if req and req.strip()]
        non_empty_role_items = [role for role in role_items if role and role.strip()]

        return render_template("job-details.html", logo=logo, logo_background=logo_background, company=company, position=position, postedAt=postedAt, contract=contract, location=location, website=website, apply=apply, description=description, requirements_content=requirements_content, requirements_items=non_empty_requirements_items, role_content=role_content, role_items=non_empty_role_items)
    
    else:
        return "Data not found"

# CREATE JOB CLASS
class Job:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.company = ""
        self.website = ""
        self.logo_background = ""
        self.posted_at = ""
        self.location = ""
        self.contract = ""
        self.position = ""
        self.description = ""
        self.requirements_content = ""
        self.requirements_items = ["", "", "", ""]
        self.roles_content = ""
        self.roles_items = ["", "", "", ""]
        self.logo_image_path = ""

    def validate_and_set_data(self, form_data):
        self.company = form_data.get("company-name", "")
        self.website = form_data.get("company-website", "")
        self.logo_background = form_data.get("company-logo-color", "")
        self.posted_at = form_data.get("job-date", "")
        self.location = form_data.get("job-location", "")
        self.contract = form_data.get("job-type", "")
        self.position = form_data.get("job-position", "")
        self.description = form_data.get("job-description", "")
        self.requirements_content = form_data.get("job-requirements", "")
        self.requirements_items = [form_data.get(f"requirements-item-{i}", "") for i in range(1, 5)]
        self.roles_content = form_data.get("job-role", "")
        self.roles_items = [form_data.get(f"role-item-{i}", "") for i in range(1, 5)]
    
    def handle_image_upload(self, uploaded_file):
        if uploaded_file:
            image = request.files["logo"]
            image.save("static/images/logos/" + image.filename)
            self.logo_image_path = f"/static/images/logos/{image.filename}"
    
    def save_to_csv(self):
        with open("./static/data.csv", "a") as file:
            file.write(
                f'{self.id},"{self.company}","{self.logo_image_path}","{self.logo_background}","{self.position}","{self.posted_at}","{self.contract}","{self.location}","{self.website}","{self.website}","{self.description}","{self.requirements_content}","{self.requirements_items[0]}","{self.requirements_items[1]}","{self.requirements_items[2]}","{self.requirements_items[3]}","{self.roles_content}","{self.roles_items[0]}","{self.roles_items[1]}","{self.roles_items[2]}","{self.roles_items[3]}"\n'
            )

# CREATE ADD JOB ROUTE AND HANDLE FORM DATA
@app.route("/add-job", methods=["GET", "POST"])
def add_job_page():
    job = Job()

    if request.method == "GET":
        return render_template("add-job.html")
    elif request.method == "POST":
        job.validate_and_set_data(request.form)
        job.handle_image_upload(request.files.get("logo"))
        job.save_to_csv()
        return redirect("/")

# RUN APP WITH DEBUG MODE
if __name__ == '__main__':
    app.run(debug=True)