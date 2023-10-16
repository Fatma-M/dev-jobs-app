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
        # Retrieve the requirements items and role items
        requirements_items = [item.get(f"requirements/items/{i}") for i in range(7)]
        role_items = [item.get(f"role/items/{i}") for i in range(5)]
        # Check if any of the requirements and role items are empty
        non_empty_requirements_items = [req for req in requirements_items if req and req.strip()]
        non_empty_role_items = [role for role in role_items if role and role.strip()]

        return render_template("job-details.html", logo=logo, logo_background=logo_background, company=company, position=position, postedAt=postedAt, contract=contract, location=location, website=website, apply=apply, description=description, requirements_content=requirements_content, requirements_items=non_empty_requirements_items, role_content=role_content, role_items=non_empty_role_items)
    
    else:
        return "Data not found"

# CREATE ADD JOB ROUTE AND HANDLE FORM DATA
@app.route("/add-job", methods=["GET", "POST"])
def add_job_page():
    if request.method == "GET":
        return render_template("add-job.html")
    elif request.method == "POST":
        id = uuid.uuid4()
        company = request.form["company-name"]
        website = request.form["company-website"]
        logo_background = request.form["company-logo-color"]
        posted_at = request.form["job-date"]
        location = request.form["job-location"]
        contract = request.form["job-type"]
        position = request.form["job-position"]
        description = request.form['job-description']
        requirements_content = request.form["job-requirements"]
        roles_content = request.form["job-role"]
        requirements_item_1 = request.form["requirements-item-1"]
        requirements_item_2 = request.form["requirements-item-2"]
        requirements_item_3 = request.form["requirements-item-3"]
        requirements_item_4 = request.form["requirements-item-4"]
        roles_item_1 = request.form["role-item-1"]
        roles_item_2 = request.form["role-item-2"]
        roles_item_3 = request.form["role-item-3"]
        roles_item_4 = request.form["role-item-4"]

        # handle image upload 
        file_name = request.files["logo"].filename
        logo_image_path = f"/static/images/logos/{file_name}"
        if "logo" in request.files:
            image = request.files["logo"]
            if image.filename != "":
                image.save("static/images/logos/" + image.filename)

        with open("./static/data.csv", "a") as file:
            file.write(f'{id},"{company}","{logo_image_path}","{logo_background}","{position}","{posted_at}","{contract}","{location}","{website}","{website}","{description}","{requirements_content}","{requirements_item_1}","{requirements_item_2}","{requirements_item_3}","{requirements_item_4}","{roles_content}","{roles_item_1}","{roles_item_2}","{roles_item_3}","{roles_item_4}"\n')

        return redirect("/")

# RUN APP WITH DEBUG MODE
if __name__ == '__main__':
    app.run(debug=True)