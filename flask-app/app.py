from flask import Flask, render_template, request
import os
import shutil
from time import sleep

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        # Receive link, check for http or https header
        website_link = request.form["link_text"]
        time_limit_str = request.form["limit"]
        if(time_limit_str != ""):
            time_limit = time_limit_str
        else: 
            time_limit = ""
        if website_link[0:4] != "http":
            website_link = "http://" + website_link 
        # Send the file, and other container should run
        with open('/usr/src/web-links/website-link.txt', 'w') as link_file:
            link_file.write(website_link)
        with open('/usr/src/web-links/time-limit.txt', 'w') as time_file:
            time_file.write(time_limit)
        # print("Checking for file...")
        # While scan runs, check for report
        # while not os.path.exists('/usr/src/web-links/file_name.txt'):
        #     print("Sleeping to wait")
        #     sleep(1)
        # print("File exists")
        # with open('/usr/src/web-links/file_name.txt', 'r') as report:
        #     file_name = report.read()
        # print(f"Using report {file_name}")
        # os.remove('/usr/src/web-links/file_name.txt')
        # shutil.copy(f"/usr/src/reports/{file_name}", f"/usr/src/app/templates/{file_name}")
        return render_template("index.html", message = f"Running scan on {website_link}")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))