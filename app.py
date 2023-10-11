from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/add-job")
def add_job_page():
    return render_template("add-job.html")


@app.route("/job-details")
def job_details_page():
    job_title = request.args.get("job-title")
    return render_template("job-details.html", job_title=job_title)
