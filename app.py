from flask import Flask, render_template, request, send_file, session
from linkedin_scraper import scrape_linkedin_jobs
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed to store data in session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    keyword = request.form['keyword']
    location = request.form['location']
    max_jobs = int(request.form.get('max_jobs', 10))

    jobs = scrape_linkedin_jobs(keyword, location, max_jobs)

    # Save results in session to use for CSV download
    session['jobs'] = jobs

    return render_template('results.html', jobs=jobs, keyword=keyword, location=location)

@app.route('/download')
def download_csv():
    jobs = session.get('jobs')
    if not jobs:
        return "No jobs to download.", 400

    # Write jobs to a temporary CSV file
    filename = "scraped_jobs.csv"
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "link"])
        writer.writeheader()
        writer.writerows(jobs)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

