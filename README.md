# Zap-Docker-App

In this project, I used Docker and Flask to build a web app that can run the [ZAP](https://www.zaproxy.org/docs/docker/full-scan/) website scanner.

The app consists of two microservices: a flask web server and the ZAP scanner, which are connected through two mounted volumes and launched with Docker Compose.

To use it, one can simply enter the website link, press submit, and the report will be rendered on the screen.

## Getting Started

1) Clone the project.

2) Set up Docker Desktop.

3) To start, run `docker-compose up`. All the volumes, images, and containers will be built automatically.

4) To enter the website link, go to `localhost:888` and follow instructions. To view the report (currently work in progress), add `/view-report` to the url, and wait for the scan to complete.

5) To stop the app, run Ctrl+C. Then, to remove the containers, run `docker-compose down`.

## How does it work

When the link is inputted into the website, it is processed by the Flask program, which enters it into a text file in a volume mount directory, and leaves a message notifying the user.

Meanwhile, the ZAP container runs a shell script on startup, which will wait for the text file containing the link to appear. 

When it does, the scanner will be run and will generate a report in another volume mount. 

While the scanner runs, the Flask app route `/view-report` will wait for the HTML report, and when it arrives, it will render it on the website at that route. 