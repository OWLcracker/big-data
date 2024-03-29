# Big Data Project

------------------------------------------------------------------------------------------------------------------------

## Overview

This submission contains the big data project for the course "Big Data and Advanced Database System Concepts",
created by Tom Schuck and Kilian Kempf at the Hochschule Karlsruhe (HKA).
Our project's objective is to leverage Apache Spark for processing data from the 
[GDELT 2.0 Event Database](https://www.gdeltproject.org/data.html#documentation) and utilize Apache Superset for data
visualization. The GDELT 2.0-Event Database is a dataset which contains
over one billion records of events from around the world. The events are collected from news articles and are updated
daily in 15-minute intervals. This rich dataset allows for the analysis and visualization of recent historical events 
worldwide, such as the conflict in Ukraine and the COVID-19 pandemic.
The dataset is available in CSV format and can be downloaded from
the [GDELT website](http://data.gdeltproject.org/gdeltv2/masterfilelist.txt).

This project encompasses two cases, both aimed at achieving the same objective through different strategies.
The first case processes and presents the data in a non-aggregated format, allowing for on-demand aggregations.
Conversely, the second case involves processing and delivering the data in a pre-aggregated format. 
Both cases are implemented and evaluated to determine the advantages and drawbacks of each approach.

The project is implemented in Python and uses the following technologies:

- [Apache Spark](https://spark.apache.org/)
- [Apache Superset](https://superset.apache.org/)
- [Jupyter Notebook](https://jupyter.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Thrift Server](https://spark.apache.org/docs/latest/sql-distributed-sql-engine.html)

In the following, both cases are explained in further detail.

### Non-Aggregated Case

The approach of the first case is to process the data in a non-aggregated form. The idea is to process the data in a way
that the data analyst can decide how the data should be aggregated for the visualization through the use of
SQL statements in Superset. The advantage of this approach is that the data analyst can decide how the data should be
aggregated. Furthermore, no data is lost to aggregation and can be displayed on demand in superset utilizing the
pre-processed data which is kept in memory in Spark.
This enables the data analyst to create visualizations that are tailored to his needs on the fly.
This is achieved by caching and processing the data in Spark. The drawback of this approach is that the processing of 
SQL requests must be executed on non-aggregated data every time a visualization is created or loaded. Depending on the
size of the data, this can take a relatively long time.

### Aggregated Case

The approach of the second case is to process the data in an aggregated form. The idea is to process the data in a way
that the data is already pre-aggregated in a suitable format for the visualization and kept in memory. The advantage of this
approach is that the processing of SQL requests is done using already aggregated data, which can result in significantly
faster response times. This is achieved by caching and processing the data in Spark. The drawback is that the aggregate
needs to be re-created every time the underlying data changes. Furthermore, the data analyst cannot create a new
aggregate on his own. This means that the data analyst has to request a new aggregation from the data engineer every 
time he wants to create a new visualization.

### Implemented Use Case

This project was developed with the example use case to analyze the Goldstein Scale values of events occurring within a
defined time period per country where the events took place.
The Goldstein Scale is a scale that measures the impact of an event. The scale ranges from -10 to +10. The higher the
value, the more positive the impact of the event. The lower the value, the more negative the impact of the event.

The goal was to visualize a world heat map that visualizes the average Goldstein Scale for each country. The
visualization should also be interactive. This means that the user should be able to filter the data, for example,
by date and country. With this, a user can, for example, analyze the impact of the corona pandemic on a country.

This use case was implemented by following the strategy of both the aggregated and the non-aggregated case.
Regarding the implementation of the non-aggregated case, the data was just pre-processed and cached in Spark without any
aggregation. By using this method, arbitrary analysis of the dataset can be conducted on demand at a fine-grained level.
To illustrate this point, the possibility was implemented in the non-aggregated case to select a country in the
dashboard and see
the top 10 events
for that country which had the most negative impact.
For the aggregated case, the data was pre-processed and aggregated by the average Goldstein Scale per country
per day. This level of aggregation was chosen to ensure that it's still possible to filter the data, which is utilized
for visualization, by date and country.

Both ways enable the user to create the desired visualization. However, which approach is better depends on multiple
factors, which will be discussed in this project.

## Table of Contents

1. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Configuration](#configuration)
    - [Setup](#setup)
2. [Usage](#usage)
    - [Web Interfaces](#web-interfaces)
    - [Run Main Code](#run-main-code)
    - [Run Test Code](#run-test-code)
    - [Create Test Result Plots](#create-test-result-plots)
    - [Superset Dashboard](#superset-dashboard)
3. [Documentation](#documentation)
    - [Architecture](#architecture)
    - [Workflow](#workflow)
    - [Limitations & Shortcuts](#limitations--shortcuts)
    - [References](#references)
4. [Analysis](#analysis)
   - [Data](#data)
   - [Scalability](#scalability)
   - [Fault Tolerance](#fault-tolerance)
5. [Evaluation](#evaluation)
    - [Non-Aggregated Case](#non-aggregated-case)
    - [Aggregated Case](#aggregated-case)
6. [Production Example & Recommendations](#production-example--recommendations)
7. [Conclusion](#conclusion)

## Getting Started

### Prerequisites

To run the project, you need to have [Docker](https://www.docker.com/get-started/) (including docker compose) installed
and running on your machine.

Additionally, make sure you are using WSL if you're running on Windows:

- Open docker desktop
- Navigate to `Settings` > `General`
- Tick the box next to `Use the WSL 2 based engine`
- Restart the docker engine

### Configuration

The spark cluster has the following configuration by default:

| Item      | Resources         | Total Resources (in cluster) |
|-----------|-------------------|------------------------------|
| Workers   | 3                 | 3                            |
| Executors | 2 per Worker      | 6                            |
| RAM       | 2 GB per Executor | 12 GB                        |
| Cores     | 1 per Executor    | 6                            |

This configuration was set as default, to ensure that the project can be run on most machines.

If you want to change the configuration, you can do so by navigating to `config` and adjust the following files:

- `spark-defaults.conf`: Contains configuration regarding the executors (total number of executors, RAM & cores per
  executor).
- `.env-spark`: Contains configuration regarding the workers (RAM & cores per worker) and must be set according to the
  executor configuration. E.g., the amount of RAM per worker must equal the amount of RAM per executor multiplied by the
  number of executors per worker.

The tests were executed with more memory assigned to the workers and executors (see [Analysis](#analysis)).

### Setup

First, you have to clone this repository.
Then open your command line and navigate to the root directory of this repository.
To set up the project, execute the following command:

```
docker compose up
```

This will automatically start and configure all necessary docker containers to run Apache Superset, Apache Spark, and a
Jupyter Server.

To shut down all containers, execute the following command:

```
docker compose down --volumes
```

## Usage

### Web Interfaces

The following web interfaces can be accessed after the setup has been completed successfully:

| Component          | URL                    | Description                                                                                                                       |
|:-------------------|:-----------------------|:----------------------------------------------------------------------------------------------------------------------------------|
| Superset Dashboard | http://localhost:8088/ | Apache Superset web interface for visualizing data processed by Spark.                                                            |
| Spark Master       | http://localhost:8080/ | Web UI for the Spark Master node, managing distributed processing jobs.                                                           |
| Spark Worker 1     | http://localhost:8081/ | Web UI for a Spark Worker node, showing details of tasks and resource usage.                                                      |
| Spark Worker 2     | http://localhost:8082/ |                                                                                                                                   |
| Spark Worker 3     | http://localhost:8083/ |                                                                                                                                   |
| Spark Application  | http://localhost:4040/ | Spark application web UI, showing details of jobs, thrift server etc. (available when a spark session is initialized in jupyter). |
| Jupyter Notebook   | http://localhost:8888/ | JupyterLab interface to interactively execute the python code of this project.                                                    |

### Run Main Code

To run the application code of the project, you have to the following steps:

1. Open the **Jupyter Notebook** web interface
2. When prompted for a token type in `token`
3. Navigate to `notebooks` > `main.ipynb`
4. Run the code cells in the notebook
5. Open the **Superset Dashboard** to view the results
6. When prompted for a login, use the following credentials:
    - Username: `admin`
    - Password: `admin`

**Don't start a separate jupyter server to run the notebook.**

### Run Test Code

1. Open the **Jupyter Notebook** web interface
2. When prompted for a token type in `token`
3. Navigate to `notebooks` > `tests.ipynb`
4. Insert test data
    1. Navigate to `notebooks` > `data` > `parquet_test`
    2. Download the ZIP file from [bwSync&Share](https://bwsyncandshare.kit.edu/s/QTKj5jtPEH3KMkF)
    3. Extract the parquet files into the `parquet_test` directory
5. If you previously ran the main code, you need to **restart the kernel**
6. Run the code cells in the notebook

**We recommend not running the test code, as the execution can take up a full day or even longer.**

### Create Test Result Plots

1. Open the **Jupyter Notebook** web interface
2. When prompted for a token type in `token`
3. Navigate to `notebooks` > `test_evaluation.ipynb`
4. Run the code cells in the notebook

### Superset Dashboard
![Superset Non-Aggregated](./misc/screenshots/superset/Dash_NAG_1.png)
![Superset Aggregated](./misc/screenshots/superset/Dash_NAG_2.png)
The previous screenshots show the dashboard of the non-aggregated case, in which the data is processed in a 
non-aggregated form. The dashboard can be accessed by clicking on `Dashboards` > `GDELT` in Superset.
The dashboard is used to visualize the average Goldstein Scale per country of all events,
which happened in the specified time period in the respective country. This aggregation must be executed on the 
non-aggregated dataset every time the dashboard is refreshed.
The dashboard is interactive, which means that the user can filter the data, for example by
date and country, by setting the filters, which can be seen on the left side of the first screenshot.
Furthermore, there is a table that shows the top 10 negative events ranked by the Goldstein Scale for the selected
dates and countries.
Moreover, the user is shown a table, which contains the average Goldstein Scale per country, sorted from the highest 
to the lowest value.
At last, the user can observe a counter which displays the total number of events for the selection.

![Superset Aggregated](./misc/screenshots/superset/Dash_Ag_1.png)
The previous screenshot shows the dashboard of the aggregated case, in which the data is already pre-aggregated
before providing it to Superset for visualization. The dashboard can be accessed by clicking on `Dashboards` > 
`GDELT Aggregated` in Superset. The dashboard serves the same purpose as the dashboard for the 
non-aggregated case: The visualization of the average Goldstein Scale per country of all events, which happened in the
specified time period in the respective country. The difference is that every time the dashboard is refreshed, the 
aggregation is executed on the already pre-aggregated dataset. Because the Goldstein Scale is already aggregated by 
country and date, the display of the top 10 negative events, like shown in the previous dashboard, is not possible. 
This is due to the fact that during the aggregation, information about the individual events is lost. If this 
was an important use case, the relevant time period would have to be known beforehand, so the top 10 events could 
be pre-selected and provided to the dashboard via a designated table.

![Superset DatabaseConnection](./misc/screenshots/superset/DB_Con.png)
The previous screenshot shows the database connection of the Superset dashboard, which can be accessed
by clicking on `Settings` > `Database Connections` > `Apache Spark SQL` in the Superset dashboard. The database 
connection is used to connect the Superset dashboards to the Spark Thrift Server. The Thrift Server provides data access
to the data which remains in Spark. This means that Superset can send SQL queries to the Thrift Server, which are processed
by Spark, to retrieve the necessary data for the visualizations. Superset utilizes a hive connection to
connect to the Thrift Server. In this case the URL is: `hive://spark@jupyter:10000`.
## Documentation

### Architecture

This section describes the architecture of the application.
![Architecture](misc/diagramms/Architectur/Architectur.png)

The application is managed through a docker-compose environment. This environment consists of the following relevant
main components: **Apache Superset**, **Apache Spark Cluster**, **Jupyter Server**, **Thrift Server**.

**Apache Superset** is a data exploration and visualization web application. It is used to visualize the data processed
by Spark. If data is required for a visualization, an SQL query is sent to the Thrift Server.

**Apache Spark** is a distributed data processing framework. It is used to pre-process the data from the GDELT dataset,
keep the result cached and process the SQL queries, which are sent by Superset.
Spark runs distributed in multiple docker containers with different roles. The **Spark Driver** is the main coordinator
of the application. It is responsible for scheduling the Jobs and catering to the requests from Superset. The **Spark Master** 
coordinates the allocation of resources in the cluster as cluster manager in standalone deployment mode. 
The **Spark Worker** is a node in the cluster that can run tasks and keep data in memory or disk storage across them.
In the architecture of this project 3 Workers are running in different containers.

**Thrift Server** is a server that enables JDBC/ODBC clients to execute SQL queries against Apache Spark.
In this case, the Thrift Server is used to enable Superset to access the data in Spark. If an SQL query is sent to the
Thrift Server, a new Spark job will be triggered. The Spark job will then retrieve the data from the cache and process
it according to the SQL-Statement. The processed data is returned to the Thrift Server, which sends a response to Superset.

**Jupyter Server** is a web application that allows you to create and share documents that contain live code, equations,
visualizations and narrative text. It is used to run the application code of the project. The application code is
written in a Jupyter Notebook. The Jupyter Server is also used to run the test code of the project.
Furthermore, the Jupyter Notebook is used to document the project and run the Spark Driver and Thrift Server.
Both the Thrift Server and the Spark Driver are started in the Jupyter Notebook because they are required to
run in the same Spark Context.

### Workflow

This section describes the general workflow of the application.

**Download Data**
![Download Data](./misc/diagramms/Fluss/DownloadFluss.png)
At first, it is necessary to download the necessary data from the GDELT server.
The basis is the [GDELT 2.0 Event Database](http://data.gdeltproject.org/gdeltv2/masterfilelist.txt) which is available
in CSV format.
The CSV files are downloaded in a compressed form and then extracted.

After extraction, the CSV files are converted into the parquet format through parallel and distributed processing
using Spark. The parquet format is a columnar storage format optimized for analytics workloads.
The resulting parquet files are stored in the local file system.

**Process Data (Non Aggregated)**  
![Process Data(Non Aggregated)](./misc/diagramms/Fluss/NonAggFluss.png)  
In the first case, the data is processed in a non-aggregated form.

The data is loaded from the parquet files that are stored on the local file system into the Spark cluster. After that, the country 
codes, which represent the location of the events, are mapped to corresponding ISO 3166-1 alpha-2 country codes.
This is necessary to visualize the data via a heatmap in the Superset dashboard, because the country codes that are 
included in the GDELT dataset are based on the FIPS10-4 standard, which is not supported by Superset.

Afterward, the resulting data is cached in memory and provisioned as a global temporary view in Spark.
By creating a global temporary view, clients can access the data by sending SQL requests to the Thrift Server.

**Process Data (Aggregated)**
![Process Data(Aggregated)](./misc/diagramms/Fluss/AggFluss.png)
For the second case, the data is processed in an aggregated form.

In the aggregated case the data is also loaded from the parquet files. After that, only the columns, which are relevant
for the desired aggregation, are selected. Rows with missing values in one of the necessary columns are dropped, since
they can't be used for the aggregation. Afterward, the data is aggregated by calculating the sum of the Goldstein Scale
value and counting the respective events grouped by country and date. This pre-aggregation provides the flexibility to
calculate the average Goldstein Scale per country for a specific time period. The country codes of the aggregated data
are then mapped to the corresponding ISO 3166-1 alpha-2 country codes.

As a final step the resulting aggregated data is cached in memory and provisioned as a global temporary view, just like
in the non-aggregated case.

**Request from SuperSet**
![Request from SuperSet](./misc/diagramms/Fluss/SuperSetFluss.png)
Another component of the application is the Apache Superset dashboard. This dashboard is used to visualize
the data processed by Spark. The dashboard is connected to the Spark Thrift Server.
This connection enables the dashboard to access the data in Spark, utilizing its distributed processing
capabilities.

When a dashboard is opened or refreshed, an SQL request is sent to the Thrift Server.
The Thrift Server then processes the SQL statement and identifies the data in the specified global temporary view.
Processing the data of the global temporary view triggers a new Spark job.
The Spark job then accesses the data, which is cached in memory, and processes it according to the SQL query.
The resulting data is then returned to the Thrift Server, who sends the requested data to the dashboard.
The dashboard then can utilize the returned data to visualize it according to the user's needs.

### Limitations & Shortcuts

**Thrift Server**  
The Thrift Server is a component of Spark that enables JDBC/ODBC clients to execute SQL queries against Apache Spark.
During the development of this project, no possiblity could be discovered to scale the Thrift Server
horizontally. Especially because it was a requirement that the Thrift Sever can access cached data registered as 
temporary views. This means that the Thrift Server is a bottleneck and single point of failure in the current architecture.
This is due to the fact that there is only a single instance of the Thrift Server, which needs to run in the same JVM 
as the Spark Driver. Future research would be necessary to either find a way to scale the Thrift Server horizontally 
or to find an alternative solution to the Thrift Server.

**Storage on Local File System**  
The data used in this project is stored in the local file system, which means that the data is neither replicated
nor distributed to different nodes, like it would be if a distributed file system like HDFS was used.
Therefore, the data storage constitutes a single point of failure as well as an I/O bottleneck.
To make the data accessible to the Spark Workers, the data is mounted into the docker containers. This means that
all Worker nodes have to read the data from the same disk, which is limited by its throughput. Therefore read operations
can't be parallelized properly, which is a bottleneck for the performance of the application.
Furthermore, the data is not fault-tolerant because the data is not replicated, which means that if the
data is lost, it is lost forever.
Therefore the solution is neither scalable nor fault-tolerant and was only chosen as a shortcut to simplify the setup
and the usage of the project. It should be further investigated if a HDFS cluster would be beneficial for this
project or if another fault-tolerant distributed file system presents a more suitable solution.

**Superset Database**  
Normally in a development environment, Superset's PostgreSQL database, which stores the configuration of the dashboards,
chart elements, etc., would be persisted using a docker volume. However, in this project
the database is persisted on the local file systen mounted into the database container. 
This solution was chosen to simplify the development and the usage of the project, because the created Superset dashboards 
can be easily exchanged between different setups using version control software like GitHub. Nevertheless, this solution
is not recommended because of synchronization issues and the potential loss of data.

**Insufficient Hardware for Tests**  
Limited by the available hardware, the scalability of the application could not be evaluated as thoroughly as desired.
In particular, the substantial resource demands of the non-aggregated approach restricted the volume of data that 
could be utilized in some test. This precaution was necessary to avoid memory problems and skewed test outcomes
due to data being cached on disk. Additionally, the application was tested on a single machine rather than on a 
multi-node cluster, which would be typically used in a production environment. By dividing the application components 
into separate docker containers, an attempt was made to mimic a cluster setting. Nonetheless, the application still
ran on shared resources throughout the testing phase. An increased overall workload on the machine could have affected the
the performance of individual components. On the other hand, the application did not face network latency or any other issues
specific to cluster environments. Therefore, the validity of the test results is limited. 


### References

The following components were taken from other sources, adapted, configured and integrated into this project:

- [Superset](https://github.com/apache/superset): The docker setup of the official Apache Superset repository is the
  foundation of the `docker-compose.yml` file and the startup scripts in the `docker` directory used in this project.
- [Spark](https://github.com/bitnami/containers/tree/main/bitnami/spark): The docker image is used to run the Spark
  Master and the Workers.
- [Jupyter](https://github.com/jupyter/docker-stacks/tree/main/images/pyspark-notebook): The docker image includes a
  Jupyter Server and an installation of Spark.
  It is used to run the application code from the notebooks of this project and to run the Thrift Server.

## Analysis

The following sections describe the results of the project analysis, which was largely conducted in the `tests.ipynb`
notebook.

### Data

The dataset which was used for the analysis of this project contains all events from the GDELT 2.0-Event Database from
July 2015 until December 2023 totaling in 102 months or 8.5 years worth of event data. As the events in the dataset
date back to the 19th of February in 2015, almost the complete dataset was included in the analysis. Events
recorded before February 2015 can be obtained from the GDELT 1.0 Event Database, which dates back to 1979. Because of
the GDELT 2.0 dataset's size and the limited resources available for the analysis, the GDELT 1.0 dataset was not
included in this project. In the following sections, mentions of a "complete" or "total" dataset refer to the 8.5 years
worth of event data that were utilized in the analysis.

The GDELT 2.0 dataset is provided in CSV files and is generated and uploaded every 15 minutes. For use in the project,
these files were downloaded and then converted to the Parquet format. This conversion reduces the required storage space
and facilitates faster data processing. The following table shows the total size of the dataset in CSV and Parquet
format:

| Total Size of CSV Files | Total Size of Parquet Files |
|-------------------------|-----------------------------|
| 185.91 GB               | 32.9 GB                     |

The previous table shows that storing the data in the Parquet format is storage space efficient and reduces the required
storage space by 82.3% for the given dataset.

After the data is loaded into Spark and pre-processed, the result is cached to enable faster access for subsequent
queries on the data by Superset. The cached data is stored primarily in memory. Once no more memory space is available,
the rest of the data is stored on disk. The following table shows the amount of data that is cached in memory and on
disk in the aggregated and non-aggregated case, when the complete dataset is used:

| Case           | Cached Data in Memory | Cached Data on Disk | Total Cached Data |
|----------------|-----------------------|---------------------|-------------------|
| Aggregated     | 0.0 MB                | 12.41 MB            | 12.41 MB          |
| Non-Aggregated | 65.39 GB              | 9.48 GB             | 74.87 GB          |

This clearly illustrates the main difference between the aggregated and non-aggregated case. In the non-aggregated case,
the space required to cache the non-aggregated data completely in memory to enable fast data processing exceeds the
memory requirements of the aggregated case in orders of magnitude. In the given example use case, the non-aggregated
case requires
6.033 times more memory than the aggregated case. This has a significant impact on the hardware, which would be required
for a cluster in a production scenario, resulting in significantly higher costs.

Furthermore, the table shows that the total data size of the cached data is 2.28 times as large as the total size of the
Parquet files, which indicates that the data, once loaded into Spark and partitioned across nodes, can't be
compressed as efficiently as it's done using Parquet files. This must also be considered when dimensioning the hardware
for the aggregated case, when the complete dataset must be cached in memory.

### Scalability

To analyze the scalability of the application, a number of tests were conducted. In these tests, the effects of
different
parameters on the performance of the application were analyzed by scaling individual parameters while keeping the rest
of the environment constant. The effect on the performance on the aggregated and non-aggregated version of the
application was measured by running both versions separately and measuring the following performance metrics:

- **Query Response Time**: The amount of time it takes for the application to process and successfully respond to an SQL
  query. This metric was chosen, because Superset sends SQL queries to the Thrift Server to retrieve data for
  visualizations.
  Therefore, the response time has a significant impact on the user experience, when the dashboard is used.
- **Pre-processing Turnaround Time**: The amount of time it takes for the application to load the necessary data from
  the local file system into the Spark Cluster, pre-process it, and cache it. This metric was chosen, because it
  represents a complete cycle of the application, from loading the data to making it available for SQL queries. This has
  an impact on how quickly data can be made available for visualizations.

In the following sections the results of the tests are presented and analyzed, in which the parameters **Data Volume**,
**Load** and **Resources** were scaled.

Unless specified otherwise in the individual test, the Spark Cluster was configured as follows for the test execution:

| Item      | Resources         | Total Resources (in cluster) |
|-----------|-------------------|------------------------------|
| Workers   | 3                 | 3                            |
| Executors | 2 per Worker      | 6                            |
| RAM       | 3 GB per Executor | 18 GB                        |
| Cores     | 1 per Executor    | 6                            |

#### Data Volume

The following tests were conducted to analyze how an increasing amount of data impacts the performance of the
application. To achieve this, the application was executed repeatedly, while incrementing the number of monthly data,
which are loaded into the cluster and processed starting at July 2015 until the complete dataset was included
(e.g., 1 month, 2 months, 3 months, ... of data). To minimize the total test duration, the measurements were done with
increasing data increments. Each measured value is depicted as a dot on the plotted lines in the following plots.
It's also important to mention that the data volume of different months can vary. For that reason, the data volume of
the months was calculated by adding the size of the included parquet files, to depict the impact of the data volume more
accurately in the plots.

The following plots illustrate the impact of an increasing data volume on the pre-processing response time of the
aggregated and non-aggregated version. The first plot depicts an increase of data up to 1 year, whereas the
following plot depicts an increase of data up to the complete dataset:

<img src="./misc/plots/data_volume_turnaround_year.png" width="2531" alt="">
<img src="./misc/plots/data_volume_turnaround_all.png" width="2554" alt="">

In both cases, it can be clearly seen that the pre-processing turnaround time increases linearly with the data volume.
This is expected for multiple reasons. First, the data volume is the main factor that impacts the time it takes to
pre-process the data. Because the number of workers and executors as well as their assigned RAM and CPU cores are kept
constant, processing the data takes longer, the more data has to be processed. Second, the data is loaded from the local
file system, which is an I/O-bound operation. In the given architecture, reading the data from disk can't be properly
parallelized, because the data is not partitioned and distributed across multiple nodes/disks, which could be read in
parallel. That means that the data has to be read sequentially and is limited by the throughput of a single disk, which
increases the duration of read operations from the disk linearly with the data volume.

Comparing the aggregated and non-aggregated version in the plots, there is a noticeable difference in the factor by
which the turnaround time increases with the data volume. On average, the turnaround time of the non-aggregated version
increases by 46.11 seconds per additional GB of data, while the turnaround time of the aggregated version only increases
by 7.07 s/GB. This can be explained by the fact that the non-aggregated version has to load and process the complete
dataset. The aggregated version, on the other hand, only has to read a small subset of the 61 columns of the dataset,
which is required for the aggregation. The additional effort, which is required to calculate the aggregation, is
presumably
offset by the reduced effort of the subsequent operations. E.g., the non-aggregated version has to join the complete
dataset with the country code mapping table, which is an expensive operation when data is partitioned and distributed,
while the aggregated version executes the join on the aggregated data. Therefore, the impact of additional data is
significantly lower in the aggregated version.

The following plots illustrate the impact of an increasing data volume on the query response time of the
aggregated and non-aggregated version:

<img src="./misc/plots/data_volume_response_year.png" width="2485" alt="">
<img src="./misc/plots/data_volume_response_all.png" width="2508" alt="">

By looking at the plots above, one can clearly notice that increasing the data volume has a significant impact on the
query response time of the non-aggregated version, while there is no or even a slight positive impact on the query
response in the aggregated version.
This can be explained by the fact that the queries sent to the Thrift Server during the
tests were the same as the ones used in the respective Superset dashboards. The queries for the non-aggregated version
therefore trigger an aggregation of the data on-demand,
which is a costly operation and requires more effort the more data has to be processed.
The query for the aggregated version, on the other hand, only has to read the already
aggregated data from the cache. The absolute size of the aggregated data is negligible; even when more data is added,
therefore the query response time is almost independent of the data volume. The slight decrease in the query response time
could be explained by the fact that the data is not partitioned when the cached aggregation result is too small (e.g.,
for 1 month of data, the aggregated data is not partitioned). Once the data is partitioned, the data can be read in
parallel by multiple executors, which might have a small positive impact on the query response time.

Upon closer examination of the non-aggregated version, a significant increase of the factor by which the query response
time grows relative to the data volume becomes evident between 7 and 8 months of data. This can be explained by the
fact that at 8 months worth of data, the available memory space is not sufficient to cache the complete dataset in
memory for the first time (indicated by the dotted red line). Therefore, the remaining data of this test run and the
additional data in the subsequent test runs are cached on disk. When an SQL query is processed, the data has to be
read from disk, which is an I/O-bound operation that increases the query response time significantly.

#### Load

The following tests were conducted to analyze how an increasing load impacts the performance of the application.
In the context of this project, an increasing number of concurrent users who are using the Superset dashboard, or an
increasing number of dashboard elements (e.g., tables, charts, etc.) can be considered as an increasing load. In both cases, 
the result would be an increasing number of SQL queries, which are sent to the Thrift Server in parallel. Therefore, the
impact of an increasing load was measured by sending an increasing number of SQL queries to the Thrift Server in
parallel and measuring how fast the Thrift Server can process and respond to the queries on average. Both versions of
the application were tested by using the same queries, which would be sent to the Thrift Server by the respective
Superset dashboard. The minimum of 1 month of data was loaded, processed and cached for the tests. This is to ensure that the
cached data fits into memory and to be able to properly scale the number of parallel queries without running into
memory issues too early.

The following plots illustrate the impact of an increasing load on the query response time of the aggregated
and non-aggregated version. The first plot depicts an increasing load of up to 100 parallel queries comparing the query
response time of both versions, whereas the following plots depict an increasing load of up to 1000 parallel queries and
their individual impact on the aggregated and non-aggregated version:

<img src="./misc/plots/load_response_both.png" width="2543" alt="">
<img src="./misc/plots/load_response_aggregated.png" width="2485" alt="">
<img src="./misc/plots/load_response_non_aggregated.png" width="2531" alt="">

In the first plot, it can be seen that the query response time of both versions increase in linear fashion with the
increasing load of up to 100 parallel queries. The factor by which the query response time increases with the load is much
higher for the non-aggregated version. This is attributed to the same factors mentioned in the previous section, such
as the increased processing effort required for on-demand data aggregation. When looking at the third plot, it can even
be noticed that the query response time of the non-aggregated version does not increase linearly, but rather
exponentially with an increasing number of parallel queries. This could be explained by the higher memory requirements
of the non-aggregated version and the limited RAM in the test environment, which has a bigger impact on the
non-aggregated version.

A critical finding from the tests is that an increase in the number of parallel queries sent to the Thrift Server not
only negatively affects the query response time but can also result in the complete failure of the Thrift Server. The
second plot shows that in the aggregated version, the Thrift Server fails to process and respond to queries once 600
queries are sent in parallel. For the non-aggregated version, the Thrift Server fails even earlier once 350 parallel
queries reach the server, which can be attributed again to the higher memory requirements. This is a critical finding
because it shows that the Thrift Server is not able to handle a high load of parallel queries, even when the data is
relatively small.
This presents a substantial limitation of the application, as no method was discovered during the research process to
horizontally scale the Thrift Server in a manner that it maintains access to the temporary views stored in memory.
Consequently, the Thrift Server constitutes both a bottleneck and a single point of failure within the application's
architecture.

#### Resources

The following tests were conducted to analyze how an increasing amount of resources impacts the performance of the
application. In the context of big data, scaling is typically achieved by adding additional nodes comprised
of commodity hardware to a cluster. To analyze this, the application was executed multiple times, each time manually
increasing the number of workers in the Spark Cluster. However, the configuration of a single worker, including the
number of executors per worker as well as the allocated RAM and CPU cores per executor, remained unchanged.

The tests were executed with the following resource configurations:

| No. Workers | Total No. Executors (in cluster) | Total RAM (in cluster) | Total No. Cores (in cluster) |
|-------------|----------------------------------|------------------------|------------------------------|
| 1           | 2                                | 6 GB                   | 2                            |
| 2           | 4                                | 12 GB                  | 4                            |
| 3           | 6                                | 18 GB                  | 6                            |

To prevent any potential side effects, the measurements were conducted with different amounts of data for the aggregated
and non-aggregated version. The non-aggregated version was tested using 2 months of data, because that is the maximum
amount that can be cached completely in memory even on a single worker node. The aggregated version was tested using 6
months of data, to make sure that the cached data is big enough to be partitioned and distributed across multiple
nodes, to see the impact of adding additional resources.

The following plot illustrates the impact of an increasing amount of resources on the pre-processing turnaround time of
the aggregated and non-aggregated version:

<img src="./misc/plots/resources_turnaround.png" width="2508" alt="">

The plot shows that the pre-processing turnaround time of the non-aggregated version clearly decreases with an
increasing number of workers. This is expected because the data is partitioned and distributed across multiple nodes,
which enables the data to be processed in parallel utilizing the additional resources. However, it is important to
note that the decrease is not liner, which is typically required in big data application, but rather logarithmic. The
root cause for this could be the I/O-bottleneck when reading the data from the local file system, which can't be
parallelized properly. The addition of nodes therefore has a diminishing effect on the pre-processing turnaround time,
when including the load time of the data from the local file system.

The impact of an increasing number of workers on the pre-processing turnaround time of the aggregated version is
significantly lower. This can also be explained by the I/O-bottleneck, but more importantly by the additional time it
takes to exchange data between the nodes. This is relevant for the aggregated case, because the aggregation, which is
done during the pre-processing phase, requires the data to be shuffled. As the data is relatively small, the additional
overhead of shuffling the data could exceed the benefits of utilizing additional resources for processing.

The following plot illustrates the impact of an increasing number of resources on the query response time of the
aggregated and non-aggregated version:

<img src="./misc/plots/resources_response.png" width="2520" alt="">

The given plot shows that the query response time of the non-aggregated version decreases with an increasing number of
workers. This is expected because the aggregation of the data is done on-demand, which can be parallelized across
multiple nodes. The additional resources therefore enable the data to be processed faster, which results in a lower
query response time. However, the decrease is again not linear, but rather logarithmic, which can be attributed to the
necessary shuffle operations (similar to the impact on the pre-processing turnaround time of the aggregated version).
For the aggregated version, the plot shows that the query response time actually increases with an increasing number of
workers. The reason for this could be that the cached data volume is so small that the overhead of reading the data
from multiple nodes exceeds the benefits of the additional resources. This is because the queries in
the aggregated version only read the already aggregated data from the cache and don't require any additional processing.

In summary, the test results show that the scalability of the application (increasing the performance by adding
additional resources) is very limited. The main reason for this is the fact that data must be read from the local file
system which constitutes an I/O-bottleneck and prevents a linear decrease of the pre-processing turnaround time.
Additionally, the overhead of shuffling the data between the nodes, which is required for the aggregation, reduces
the benefits of adding additional resources, especially when the amount of data is rather small. Another factor which
limits the scalability is the Thrift Server, which can't be scaled at all and therefore represents a bottleneck
for incoming queries.

In general, more tests would be necessary to more accurately measure the scalability of the application. Leveraging
additional hardware would enable the exploration of a wider range of cluster configurations with larger amounts of data
that could be fully cached in memory.

### Fault Tolerance

The following tests were conducted to analyze the fault tolerance of the application. This is important because the
application should be able to handle the failure of individual nodes and the contained data without having to process
the complete dataset from scratch again. To measure the impact of failing nodes, the application was executed multiple
times, each time manually stopping a different number of workers in the Spark Cluster after the data has
been pre-processed and cached. This leads to the loss of cached data partitions, which have to be reproduced once a
query is sent to the Thrift Server, which requires all partitions to be available. Like in the resource scalability
tests, 1 month of data was used for the non-aggregated version and 6 months of data for the aggregated version, to
ensure that the cached data fits into memory and that the cached data is big enough to be partitioned and distributed
across all nodes, to see the impact of stopping workers.

The following screenshots illustrate the impact on the cached data of the aggregated version, when stopping 0, 1 and 2
out of 3 workers in the Spark Cluster:

All workers running with 100% of the data cached in 6 partitions:
<img src="./misc/screenshots/spark/stopped_workers_0.png" width="100%" alt="">
One worker stopped with 66.67% of the data cached in 4 partitions:
<img src="./misc/screenshots/spark/stopped_workers_1.png" width="100%" alt="">
Two workers stopped with 33.33% of the data cached in 2 partitions:
<img src="./misc/screenshots/spark/stopped_workers_2.png" width="100%" alt="">

The following plot illustrates the impact of failing workers on the query response time of the aggregated version:

<img src="./misc/plots/fault_tolerance_response.png" width="2508" alt="">

As the plot shows, that queries sent to the Thrift Server are still processed and responded to, even when workers are
stopped. However, the query response time increases by orders of magnitude. This is expected 
because the partitions, which are lost due to the failed workers, have to be re-loaded from the local file system and
processed again.

This emphasizes two important characteristics of Spark:

- **Lineage Graph**: Spark keeps track of the operations that are performed on the data, which enables it to re-create
  lost partitions by re-executing the operations that were performed on the individual partitions.
- **Lazy Evaluation**: Spark only processes the data when it is required, which enables it to re-create lost partitions
  only when they are needed.

This means that the application is fault-tolerant because it can re-create lost partitions and is therefore able to
successfully respond to queries, even when workers containing needed partitions are stopped. The downside of the
re-creation of data is Spark's lazy evaluation mechanism, since the data is not re-created right away, but only when
a query is sent to the Thrift Server, which can result in a significant increase of the query response time for the user
which sent the query.

The Thrift Server, on the other hand, as it was already mentioned, acts as a single point of failure in the application.
It can't be replicated to ensure that queries can be processed and responded to, even when an instance of the
Thrift Server fails.

## Evaluation

### Non-Aggregated Case

Whether the non-aggregated case is more suitable than the aggregated case depends on the use case. The non-aggregated case is better
if the data
analyst wants to analyze the data in a fine-grained way. This is because the data is not aggregated and can be analyzed
on the fly using arbitrary queries. Furthermore, no data engineer is required to aggregate the data for the data analyst. This means that
the data analyst can create visualizations that are tailored to his needs without depending on a data engineer.
However, the drawback is that the data needs to be processed every time a visualization is created or loaded. This can
take a relatively long time depending on the size of the data and can be quite resource-intensive.

In terms of hardware, the non-aggregated is more expensive than the aggregated approach. This is because the data needs
to be
processed every time a visualization is created or loaded. This means that more data needs to be processed more often
than in the aggregated case and that significantly more memory is required. This is due to the fact that the whole 
dataset must be cached in memory to be processed quickly, to respond to queries in a reasonable time.
Therefore the non-aggregated case is more expensive in terms of hardware but cheaper in terms of development costs.

| Pros                        | Cons                 |
|-----------------------------|----------------------|
| Flexible analytical queries | Expensive            |
| Fine-grained data access    | Long execution times |
|                             | Resource intensive   |
|                             | Complex to work with |

### Aggregated Case

Whether the aggregated approach is a more suitable solution than the non-aggregated approach depends also on the 
use case. The aggregated approach is better if the data
analyst wants to analyze the data in an aggregated way. This is because the data can be pre-processed and aggregated
specifically beforehand and can be visualized immediately. Because the processing of the smaller dataset is less
resource
intensive, the overall costs decrease while the performance increases. Furthermore, the data analyst does not need
to think about
processing the whole dataset but can focus on only the necessary already aggregated data. The drawback is that the data
needs to be processed again every time the data changes. Furthermore, the data analyst cannot decide how the data should
be aggregated. This means that the data analyst has to request a new aggregation from a data engineer every time he
wants to create a new visualization.

In terms of hardware, the aggregated case is cheaper than the non-aggregated. This is because the data is already
aggregated and
does not need to be processed extensively every time a visualization is created or loaded. The memory usage only spikes 
when aggregates are created and the data is cached. 
Subsequently, memory usage significantly decreases in comparison to the non-aggregated case, as the aggregated data 
occupies far less space than the raw data. This is under the assumption that the aggregation is not
time-critical and can be done in advance.
Therefore the aggregated case is cheaper in terms of hardware but more expensive in terms of development costs.

| Pros                  | Cons                        |
|-----------------------|-----------------------------|
| Short execution times | Dependant on data engineer  |
| Easy to work with     | Reprocessing on data change |
| Cost efficient        | Aggregation takes time      |
| Resource efficient    |                             |

## Production Example & Recommendations

Based on the results of the analysis, the following example illustrates how the application could be used in a
production environment, what improvements of the architecture could be made and what the costs of the setup would be.

In this example, it is to be assumed that there is a company that wants to analyze the GDELT dataset in a way so that
they can analyze the impact of global events on their and other businesses. For example a dashboard could be created,
which contains indicators and visualizations regarding specific types of events that are aggregated by country, which could
then be compared to the company's sales data to see if there is a correlation between the events and the sales in 
affected countries. 

The company has a data science team that is responsible for analyzing the data and a data engineering team that is
responsible for preparing the data to fitting aggregates for the data science team to analyze.

Through the results of this project, the company decides to use the aggregated approach to analyze the data, due
to the cost- and resource-efficiency of the approach compared to the non-aggregated approach.
Furthermore, they
came to the conclusion that aggregated data is sufficient for their use case and that they don't need to analyze the
data in a fine-grained way.

The company decides to use the following architecture to analyze the data, which is based on the architecture of this
project:  
![Production Example](./misc/diagramms/Architectur/Architecture-AWS.png)

The company decides to use AWS as a cloud provider, to avoid the need to manage the infrastructure and to be able to
scale the infrastructure based on their needs.

In the proposed architecture, the data is stored in Elastic Block Store (EBS) volumes.
EBS volumes are block-level storage volumes that can be attached to EC2 instances. EBS volumes are highly available and
redundant, which means that the data is fault-tolerant and can be recovered if a failure occurs.
This is an important improvement over the local file system, which was used in the project, as it also enables
reading data in parallel fashion. It is estimated that about
150GB of storage space is required to store the raw data in a compressed format as well as the aggregated data 
in the EBS volumes. The business data, however, is not considered in this estimation. The data is stored in EBS using the
parquet file format, because it is a columnar storage format optimized for analytics workloads.

The data engineering team works with a m4.xlarge EC2 instance in which a Jupyter server is running. The Jupyter
server is used to run the application code of the project. The instance is configured with 16GB of RAM and 4 vCPUs.

Furthermore, the data engineering team utilizes an AWS EMR cluster. EMR is a managed cluster platform that simplifies 
running big data frameworks, such as Apache Spark, Apache Hadoop, Apache Hive, and Apache Kafka, on AWS to process 
and analyze vast amounts of data. The EMR cluster is be configured with four r4.xlarge EC2 instances. Each instance is
configured with 30GB of RAM and 4 vCPUs. The master node will be a m4.large EC2 instance. The master node is configured with
8GB of RAM and 2 vCPUs, as it is only responsible for managing the cluster and does not process any data itself.

In this setup, the data engineering team plays a crucial role in preprocessing the data into appropriate 
aggregates for analysis by the data science team. Utilizing a Jupyter server, the data engineering team executes the
project's application code and oversees the management of the EMR cluster. The EMR cluster leverages EBS volumes for
both accessing raw data and storing the processed, aggregated data.

It is estimated that the pre-aggregated data is small enough that big data frameworks like Spark are not necessary to
to process data in a distributed way, when analytical SQL queries are executed on this data. 
Rather, the data can be processed utilizing traditional processing frameworks and SQL engines.
Because of this, the Thrift Server is no longer necessary as the data doesn't need to be stored in Spark, removing the 
non-scalable bottleneck from the architecture. Instead the data analysis team utilizes a m4.xlarge EC2 instance in 
which an Apache Superset and an Apache Hive instance are running.
The Hive instance can load the data from the parquet files which are stored in the EBS volumes and provides a HiveQL interface
which can be queried. Superset is then able query the data by sending requests to the Hive instance and visualize the 
results.

The cost of this setup is estimated to be about 786.18$ per month. This includes the costs for the EBS volumes, the
EC2 instances, and the EMR cluster. The costs for the EBS volumes are estimated to be about 17.85$ per month. The costs
for the EC2 instances are estimated to be about 175.20$ per month. The costs for the EMR cluster are estimated to be
about 593.13$ per month. The costs for the EMR cluster are estimated to be so high, because the cluster is configured with
a lot of memory. This is due to the fact that the cluster was configured to be able to process the whole dataset at once,
to ensure that even large amounts of data can be processed quickly. These costs could be reduced by using a smaller 
cluster and by processing the data in batches. However, this would increase the turnaround time of the data processing.


The costs for the EMR cluster were calculated with the rough estimation that they will be running for about 10 hours per
day, since the cluster is only used to process the data and can be shut down once the data is prepared.
The costs for the Superset instance were calculated assuming a runtime of 24 hours per day, to ensure that the 
visualizations can be accessed at any time.

## Conclusion

The comparison of the non-aggregated and the aggregated implementation of the application clearly shows, that the 
additional flexibility of the non-aggregated version is outweighed by its significantly higher resource requirements
and the corresponding costs. Using the non-aggregated approach a data analyst could analyze the data in a more flexible
manner, because he would be able to execute arbitrary analytical queries on-demand without the need to prepare a designated
aggregation beforehand. However, to retrieve the result in a reasonable time, the complete dataset would have to be
cached in memory, so Spark can process the data quickly. This would require an enormous amount of memory, leading to
exploding hardware costs. Furthermore, this approach is more sensitive to an increasing load, because every request 
triggers a Spark job executing a potentially expensive aggregation on the complete dataset. An increasing
amount of users would quickly lead to an overload of the Spark cluster and a significant increase of the query response
time.

The aggregated approach, on the other hand, is more resource- and cost-efficient, because the data only needs to be
prepared once and can be efficiently queried by subsequent requests. Even when additional processing of the pre-aggregated
data is needed to fulfill a request, the amount of data that would need to be processed would be significantly smaller 
and therefore less resource-intensive. This would lead to a more stable and predictable query response time, even when 
the load increases. In addition to that, the query response time is almost independent of the data volume. Only the 
one-time effort to prepare the data increases. The amount of RAM that is required to cache pre-aggregated data entirely
in memory is significantly smaller compared to the non-aggregated case, resulting in notably lower hardware costs. The 
drawback of the aggregated approach is the time and effort it takes to prepare the data. The analysis would be limited
to the data which is already prepared and therefore less flexible. 

However, both approaches suffer from the identified weaknesses of the architecture. As no way could be identified 
to scale the Thrift Server horizontally, it constitutes a bottleneck and a single point of failure and is therefore
not suitable to be used in a production environment. Furthermore, the data is read from the local file system, which is 
detrimental to the scalability and fault tolerance of the application. Further research would be necessary to determine
whether the application could be properly scaled, when a distributed file system (e.g. HDFS) would be used to store the data.
Additionally, the usage of the Thrift Server needs further investigation to determine if there is a way to scale it 
or whether there is a substitute, which provides the required functionality. 

Considering the identified drawbacks of the prototyped architecture, a more suitable solution was proposed in the 
[production example](#production-example--recommendations), which differs from the implemented prototype.
The proposed architecture leverages cloud services to run the application in a scalable and fault-tolerant way, while 
keeping the costs at a reasonable level. This is due 
to the fact that the RAM- and CPU-intensive cluster, which is used to run Spark, is only needed for processing and 
preparing required aggregates
and can be shut down once the data is prepared. For querying the data a single instance of Hive should be sufficient, 
because processing pre-aggregated data is relatively cheap and doesn't require the data to be stored in memory 
and to be processed by the use of distributed computing.
The data could be stored in EBS volumes, which are fault-tolerant and don't present an I/O-bottleneck for the application.

Therefore the proposed architecture provides an elastically scalable, fault-tolerant and cost-efficient solution, which 
retains the visualization capabilities of Superset and the distributed data processing capabilities of Spark for the
resource-intensive pre-processing.
