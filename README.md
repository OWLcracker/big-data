# Big Data Project

<!--- TODO: add short summary of the project --->

## TODO
- [] Tests erstellen
   - [] Scalability (load, queries) -> Gleiche Datenmenge, alles In-Memory, Requests in parallelen Threads, Average pro Request
   - [] Scalability (n worker) -> Gleiches Setup, unterschiedliche Anzahl an Worker, alles In-Memory
   - [] Scalability (data) -> Unterschiedliche Datenmengen, RAM als bottleneck
   - [] Fault tolerance (kill worker)
- [] Tests ausführen
- [] Jupyter Notebook Markdown Erklärungen
- [] Diagramme von Testergebnissen
- [] Daten bereitstellen & Einfügen ermöglichen
- [] Github Readme
  - [] Nutzungsanleitung anpassen -> Daten reinziehen, Kernel restarten
  - [] References (Superset Docker Compose, Bitnami Docker Images)
  - [] Untersuchungen/Erläuterungen in Readme integrieren 
- [] Erläuterungen
  - [] Prototyp
     - [] Architektur
     - [] Workflow
     - [] Superset Dashboard
  - [] Case
    - Big Data (Warum Big Data Case? Warum nicht mit traditionellen Lösungen umsetzbar) 
    - Verteilung, Parallelisierung, Skalierbarkeit, Fault Tolerance, Data Storage
    - Shortcuts/Limitations
  - [] Skalierbarkeit
    - Auswirkung zusätzlicher Daten/Queries ~ Ressourcen
    - Datenfluss (IO-/Memory-/CPU-bound)
    - Skalierbarkeit der einzelnen Abschnitte
    - Partitionierung
    - Dimensionierung für Realität (Kosten, Aufwand, Expertenwissen, Hardware)
  - [] Fault Tolerance
    - Verhalten bei Fehlern (kill Node)
    - Verhalten Netzwerkunterbrechung
    - Auswirkung von Fehleroleranzmechanismen auf System
- [] Ausblick
  - [] Reale Architektur (inkl. beteiligter Personen, Komponenten, Hardware) -> Parquet File(s) in HDFS Cluster

## Table of Contents

1. [Getting Started](#getting-started)
    - [Prerequesites](#prerequesites)
    - [Setup](#setup)
2. [Usage](#usage)
    - [Web Interfaces](#web-interfaces)
    - [Run Code](#run-code)
3. [Documentation](#documentation)
    - [Spark](#spark)
    - [Superset](#superset)
    - [Jupyter](#jupyter)

## Getting Started

### Prerequesites

To run the project you need to have [Docker](https://www.docker.com/get-started/) (including docker compose) installed
and running on your machine.

Additional make sure your are using WSL if you're running on Windows:

- Open docker desktop
- Navigate to `Settings` > `General`
- Tick the box next to `Use the WSL 2 based engine`
- Restart the docker engine

<!---
Additionally you need to allow docker to access the files in this repository:

- Open docker desktop
- Navigate to `Settings` > `Ressources` > `File sharing`
- Add the file path to the repository 
--->

### Setup

First you have to clone this repository.
Then open your command line and navigate to the root directory of this repository.
To setup the project, execute the following command:

```
docker compose up
```

This will automatically start and configure all necessary docker containers to run Apache Superset, Apache Spark and a
Jupyter Server.

To shut down the all containers, execute the following command:

```
docker compose down --volumes
```

## Usage

### Web Interfaces

The following web interfaces can be accessed after the setup has been completed successfully:

| Component          | URL                    | Description                                                                                                                       |
|:-------------------|:-----------------------|:----------------------------------------------------------------------------------------------------------------------------------|
| Superset Dashboard | http://localhost:8088/ | Apache Superset web interface for visualizing data processed by spark.                                                            |
| Spark Master       | http://localhost:8080/ | Web UI for the Spark master node, managing distributed processing jobs.                                                           |
| Spark Worker 1     | http://localhost:8081/ | Web UI for a Spark worker node, showing details of tasks and resource usage.                                                      |
| Spark Worker 2     | http://localhost:8082/ |                                                                                                                                   |
| Spark Worker 3     | http://localhost:8083/ |                                                                                                                                   |
| Spark Application  | http://localhost:4040/ | Spark application web UI, showing details of jobs, thrift server etc. (available when a spark session is initialized in juypter). |
| Juypter Notebook   | http://localhost:8888/ | JupyterLab interface to interactively execute the python code of this project.                                                    |

### Run Code

To run the application code of the project you have to to the following steps:

1. Open the **Jupyter Notebook** web interface
2. When prompted for a token type in `token`
3. Navigate to `notebooks` > `main.ipynb`
4. Run the code cells in the notebook
5. Open the **Superset Dashboard** to view the results
6. When prompted for a login use the following credentials:
    - Username: `admin`
    - Password: `admin`

**Don't start a seperate jupyter server to run the notebook.**

## Documentation

### Spark

### Superset

### Jupyter


<!---
## Notes

Connection URI from Superset to the Thrift Server

```
hive://spark@jupyter:10000/default

find [directory] -type d -empty -exec touch {}/.gitkeep \;

```
--->