from flask import Flask, render_template, request
import socket # for TCP connections with the ZAP container
import os
import shutil

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        # Receive link, check for http or https header
        website_link = request.form["link_text"]
        if not website_link.startswith("http"):
            website_link = "https://" + website_link 

        # Send the link to the zap-scanner via a data buffer using sockets over the docker network
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('zap-scanner', 3030))  # Connect to zap-scanner service
                sock.sendall(website_link.encode('utf-8'))  # Send the link
                response = sock.recv(1024)  # Receive response
                scan_status = response.decode('utf-8')
        except Exception as e:
            scan_status = f"Error sending link: {e}"

        return render_template("index.html", message = f"Running scan with {scan_status}, visit /view-report")
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