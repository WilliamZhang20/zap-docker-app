# Zap-Docker-App

In this project, I used Docker and Flask to build a web app that can run the [ZAP](https://www.zaproxy.org/docs/docker/full-scan/) website scanner.

The app consists of two microservices: a flask web server and the ZAP scanner, which are connected through two mounted volumes and launched with Docker Compose. 

To use it, one can simply enter the website link, press submit, and the report will be rendered on the website.

## Getting Started

1) Clone the project.

2) Set up Docker Desktop.

3) To start, run `docker-compose up`. All the volumes, images, and containers will be built automatically.

4) Go to `localhost:8888` and follow instructions. To view the report, add `/view-report` to the end of the URL, and wait for the scan to complete.

5) To stop the app, run Ctrl+C in the terminal. Then, to remove the containers, run `docker-compose down`.

## How does it work?

When the link is inputted into the website, it is processed by the Flask program, which enters it into a text file in a volume mount directory, and leaves a message notifying the user.

Meanwhile, the ZAP container runs a shell script on startup, which will wait for the text file containing the link to appear. 

When it does, the link will be collected, the ZAP scanner will be run, and the report HTML will be generated in another volume mount.

While the scanner runs, the Flask app route `/view-report` will wait for the HTML report, and when it arrives, it will render it on the website at that route. 

## Important Notes

When entering the link, be sure to **omit 'www' or any other similar subdomains**. Retaining it will often cause the ZAP to run indefinetly at extremely high CPU usage. The best way to avoid this is by selecting and copying the link on Chrome, which will always be suitable. 

The ZAP scanner will take approximately 3-5 minutes to run, depending on your machine's performance and the number and severity of alerts. If it runs for more than 8 minutes with over 1000% in container CPU usage, or for more than 15-20 outright, there is likely a bug. 

One can download the report by simply right-clicking and saving the website as an HTML. 

When the scan is complete and the report is generated, the app will need to be stopped before another scan can be run. This is due to the ZAP container exiting immediately after a report is generated. 

## Next Steps

1) Implementing REST API or a Kubernetes cluster to orchestrate the contianers.  
2) Deploying it to a production environment like AWS to make the website public.
3) Allowing for more options in the UI, such as adding the AJAX spider, choosing baseline/full scan, etc.