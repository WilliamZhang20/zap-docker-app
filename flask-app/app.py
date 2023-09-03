from flask import Flask, render_template, request
import os
import shutil

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        # Receive link, check for http or https header
        website_link = request.form["link_text"]
        if website_link[0:4] != "http":
            website_link = "http://" + website_link 
        # Send the file, and other container should run
        with open('/usr/src/web-links/website-link.txt', 'w') as link_file:
            link_file.write(website_link)
        return render_template("index.html", message = f"Running scan on {website_link}, visit /view-report")
    return render_template("index.html")

@app.route('/view-report', methods = ["GET"])
def render_report():
    file_name = "my_zap_report.html" # changed to generic name
    if os.path.exists(f'/usr/src/reports/{file_name}'):
        shutil.copy(f'/usr/src/reports/{file_name}', f'/usr/src/app/templates/{file_name}')
        return render_template(file_name)
    else:
        return "Report not available yet, please wait"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))