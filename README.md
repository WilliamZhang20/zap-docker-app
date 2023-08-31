# Zap-Docker-App

In this project, I used Docker and Flask to build a web app that can run the [ZAP](https://www.zaproxy.org/docs/docker/full-scan/) website scanner.

The app consists of two microservices: a flask web server, and the ZAP scanner, which are connected through two mounted volumes and started with Docker Compose.

To use, one can simply enter the website link, press submit, and the report will be rendered on the screen.

## Getting Started

1) Clone the project

2) Set up Docker Desktop

3) To start, run `docker-compose up`. All the volumes, images, and containers will be built automatically.

4) To stop, run Ctrl+C. Then, to remove the containers, run `docker-compose down`.

## How does it work

When the link is inputted into the website, it is processed by the Flask program, which enters it into a text file in a volume mount directory.

Meanwhile, the ZAP container runs a shell script on startup, which will wait for the text file containing the link to appear. 

When it does, the scanner will be run. 