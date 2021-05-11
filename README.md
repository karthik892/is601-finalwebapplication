# Project Description

This is the final project for the course IS 601 - Web Systems Development.

In this project, the code from the previous homework assignment ([here](https://github.com/karthik892/is601-WebApplicationHomeworkPart4.git)) is expanded upon to add the following features:

- A chart to display statistics
- A user authentication system with support for user registration and e-mail verification

# Team members

While thisproject was initially intended to be completed by a group of 2 people. Circumstances have required me to complete this entire project on my own.
- Karthik Sankaran


# Running the application

## Obtain a sendgrid API key
Create a ```.env``` file in ```app/MLBPlayers``` with the following contents:
```
SENDGRID_API_KEY="your-key-here"
```

## Insert .env file
If you are the instructor who is grading this project, use the ```.env``` file provided as part of the submission and place it in the ```app/MLBPlayers``` directory as described in the project report.

## Run docker-compose

You need to have [docker desktop](https://www.docker.com/products/docker-desktop) installed to run this application.

NOTE: On Window 10, you will need to have WSL2 installed in order to run docker (but the installation should guide you through this process)

To run the application run the following command.

```
docker-compose up
```

If you want the application to run in the background use:

```
docker-compose up -d
```