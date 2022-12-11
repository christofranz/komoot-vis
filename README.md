# komoot-vis


### Table of Contents

1. [About Map-App](#about)
2. [Installation and Instructions](#installation)
3. [File Descriptions](#files)
4. [Licensing, Authors and Acknowledgements](#licensing)

## About komoot-vis<a name="about"></a>
This application allows you to query your tour data from komoot and index it with Elasticsearch for a subsequent visualization in Kibana. Query results from Komoot-Api contain much meta data as the tour type, duration, distance and the coordinates. Afterwards you can use this data to create your own dashboard in Kibana. See <a href="https://www.elastic.co/guide/en/kibana/current/docker.html">https://medium.com/@franzke.christoph/create-your-own-komoot-dashboard-6a0cd35ab89</a> for more details how to do this.

## Installation and Instructions<a name="installation"></a>
The python scripts and jupyter notebooks requires certain packages to be installed. All dependencies can be installed with python3 and the requirements.txt into a virtual environment via

`pip install -r requirements.txt`

once you created and activated a virtual environment for python3.

There are different ways to get elasticsearch and kibana running. An easy way is to work with the provided docker images and follow the steps <a href="https://www.elastic.co/guide/en/kibana/current/docker.html">here</a>.

Create the network and get the docker up and running for elasticsearch:
  

<code>docker network create elastic <br>
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.3.3 <br>
docker run --name es-node01 --net elastic -p 9200:9200 -p 9300:9300 -t docker.elastic.co/elasticsearch/elasticsearch:8.3.3</code>
  
Now the docker for Kibana:
  
<code> 
docker pull docker.elastic.co/kibana/kibana:8.3.3 <br>
docker run --name kib-01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.3.3
</code>
  
Now you can enter your e-mail and pwd of Komoot in `query_data.py`. Afterwards you can simply run the main script with `python query_data.py` to fetch all your komoot tour details. In the second step run the `elk-preprocessing.ipynb` to index your data with elasticsearch. Then you are set up and can create your own dashboard for komoot tour data analytics (see link above for more details).

## File Descriptions<a name="files"></a>
The most important files and folders in this repository:

* `api.py` - Contains the functions to connect with the Komoot-Api and fetch data from it.
* `query_data.py` - Main script to connect with Komoot and store the tour data locally.
* `elk-preprocessing.ipynb` - Notebook to process and index the data for Kibana.

## Licensing, Authors and Acknowledgements<a name ="licensing"></a>
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)