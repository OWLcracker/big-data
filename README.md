# Big Data Project

<!--- TODO: add short summary of the project --->

## Table of Contents

1. [Getting Started](#getting started)
    - [Prerequesites](#prerequesites)
    - [Setup](#setup)
2. [Usage](#usage)
3. [Documentation](#documentation)
    - [Spark](#spark)
    - [Superset](#superset)
    - [Jupyter](#jupyter)

## Getting Started

### Prerequesites

To run the project you need to have [Docker](https://www.docker.com/get-started/) (including docker compose) installed and running on your machine.

Additional make sure your are using WSL if you're running on Windows:
- Open docker desktop
- Navigate to `Settings` > `General`
- Tick the box next to `Use the WSL 2 based engine`
- Restart the docker engine
<!---
Additionally you need to allow docker to access the files in this repository:

- Open docker desktop
- Navigate to `Settings` > `Ressources` > `File sharing`
- Add the file path to the repository --->

### Setup

First you have to clone this repository.
The open your command line and navigate to the root of this repository.
To setup the project, execute the following command:

```
docker compose up
```

This will automatically start and configure all necessary docker containers to run Apache Superset, Apache Spark and a
Jupyter Server.

To shut down the all containers, execute the following command:

```
docker compose down
```

## Usage

The following UI components can be accessed:

| Component          | URL                    | Description                                                                                                                       |
|:-------------------|:-----------------------|:----------------------------------------------------------------------------------------------------------------------------------|
| Superset Dashboard | http://localhost:8088/ | Apache Superset web interface for visualizing data processed by spark.                                                            |
| Spark Master       | http://localhost:8080/ | Web UI for the Spark master node, managing distributed processing jobs.                                                           |
| Spark Worker       | http://localhost:8081/ | Web UI for a Spark worker node, showing details of tasks and resource usage.                                                      |
| Spark Application  | http://localhost:4040/ | Spark application web UI, showing details of jobs, thrift server etc. (available when a spark session is initialized in juypter). |
| Juypter Notebook   | http://localhost:8888/ | JupyterLab interface to interactively execute the python code of this project.                                                    |

## Documentation

### Spark

### Superset

### Jupyter

## Notes

Connection URI from Superset to the Thrift Server

```
hive://spark@jupyter:10000/default
```
