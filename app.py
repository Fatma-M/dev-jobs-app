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
@app.route("/job-details")
def job_details_page():
    return render_template("job-details.html")

# RUN APP WITH DEBUG MODE
if __name__ == '__main__':
    app.run(debug=True)
