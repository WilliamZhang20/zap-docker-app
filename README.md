# Zap-Docker-App

In this project, I used Docker and Flask to build a web app that can run the [ZAP](https://www.zaproxy.org/docs/docker/full-scan/) website security scanner.

The app consists of two container-based microservices: a Flask web server and the ZAP scanner, which are connected through two mounted volumes and launched with Docker Compose. 

To use it, one can simply enter the website link, press submit, and the security scan report will be rendered on the browser.

## Getting Started

1) Clone the project.

2) Set up Docker Desktop.

3) To start, run `docker-compose up` from the directory of the project. All the volumes, images, and containers will be built automatically.

4) Open `localhost:8888` in a browser, enter the link (see Important Notes below), and press submit. To view the report, add `/view-report` to the end of the URL, and wait for the scan to complete.

5) To stop the app, run Ctrl+C in the terminal. Then, to remove the containers, run `docker-compose down`.

## How does it work?

When the link is inputted into the website, it is processed by the Python script `/flask-app/app.py`, which enters it into a text file within a Docker Volume-mounted directory, and leaves a message notifying the user.

Meanwhile, the ZAP container runs a shell script on startup, which will wait for the text file containing the link to appear. 

When it does, the link will be collected, the ZAP scanner will be run, and the report HTML file will be generated in another volume-mounted directory.

While the scanner runs, the Flask app route `/view-report`, controlled by the same Python script, will wait for the HTML report to be created, and when it exists, the Flask program will render it on the website at that route. 

## What does each file do? 

The file `/compose.yaml` in the root directory is a YAML configuration file that is run upon the terminal command `docker-compose up` in the same directory, and launches both microservices with the appropriate ports, Docker Volumes, and root user settings.

The file `/flask-app/templates/index.html` has the contents of the main web page in the front end as part of the original Flask app route.

The Python script `flask-app/app.py` is the meat of the whole project. It will take the URL from the input line on the home page and send it to the other container. At the same time, the route `/view-report` in the same script will check if the HTML report from the scanner appears. If not, a simple message will be displayed on the screen. However, if it does and the website is accessed, then the HTML-based report will be copied to the frontend container's directory and rendered onto the route page.

The file `flask-app/Dockerfile` copies the directory files into the container, installs Python, Flask (version specified in `requirements.txt`), and pip, configures the Docker network port needed, and runs `app.py`, which initiates and allows everything else in the container to be executed. 

The Bash script `zap-scanner/scan-script.sh` waits for the text file containing the URL to be created by the Python script in the other container to appear in the volume-mounted directory. So long as it does not exist, it will sleep for one second and check again in an infinite loop. However, as soon as it does, the script will run the ZAP scanner using a terminal command with special flags to run it on the given URL and to generate a report in the desired directory. 

The file `zap-scanner/Dockerfile` installs all necessary files required for the scanner, as provided on [Docker Hub](https://hub.docker.com/r/owasp/zap2docker-stable). Then, it copies my Bash script into it, and immediately executes the script, which will initially run at the same time as the Python script from the other container. 

## Issues Encountered

During the process of learning Docker and the usage of the ZAP scanner, I first had to go from running the scanner in Docker using ZAP's GUI, to simply calling it and using ZAP's custom Docker CLI commands and receiving security reports in the terminal. This involved figuring out which flags served which purpose and the order required. Afterwards, I needed to set up a volume for the container so that the report would remain even once the container stopped running.

The next difficult part was to link the containers so that the URL could be passed between them. The most advanced way would definitely be to set up an API. However, I decided to take a shortcut by simply linking them with another volume that contained a text file with the link. Once the idea had been discovered, implementing it was easier as it was simple file management.

Finally, I had to render the report to the user in the browser. Unfortunately, rendering it on the same app route that the user entered the link did not work, so after some trials, the working result had to keep the original website based on the same HTML file, split the app into another specialized route, which could either have simple non-HTML text to simply indicate no report was available yet, or render the entire report. Another major error was that entering 'www' based URLs made the scanner run indefinitely, possibly due to  the scanner itself or the CLI-based execution. For example, entering "www.google.com" was problematic, but simply "https://google.com" was good. 

## Important Notes

When entering the link, be sure to omit 'www' or any other similar subdomains. Retaining it will often cause the ZAP to run indefinitely at extremely high CPU usage. The best way to avoid this is by selecting and copying the link on Chrome, which will always be suitable. 

The ZAP scanner will take approximately 3-5 minutes to run, depending on your machine's performance and the amount and severity of alerts. If it runs for more than 8 minutes with over 1000% in container CPU usage, or for more than 15-20 outright, there is likely a problem. 

One can download the report by simply right-clicking and saving the website as an HTML. 

When the scan is complete and the report is generated, the app will need to be stopped before another scan can be run. This is due to the ZAP container exiting immediately after a report is generated. 

## Next Steps

1) Implementing REST API or a Kubernetes cluster to orchestrate the containers.  
2) Deploying it to a production environment like AWS to make the website public.
3) Allowing for more options in the UI, such as adding the AJAX spider, choosing baseline/full scan, etc.
