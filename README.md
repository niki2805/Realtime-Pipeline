# Streaming Data Pipeline

A data pipeline that can ingest streaming analytics data like user interactions using Kafka, Spark, Cassandra and
Presto.

## Requirements

1. Docker
2. Python 3.10

## Init

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Kafka

Start Kafka and Zookeeper

```sh
docker compose up -d zookeeper broker
```

## Run Cassandra

Start a 3-node Cassandra cluster :

```sh
docker-compose up -d cassandra-1 cassandra-2 cassandra-3
```

Check Cassandra cluster status:

```sh
docker-compose exec -it cassandra-1 bash -c 'nodetool status'
```

Execute 'cassandraCQLScript.cql' script to create keyspaces for different categories of events with replication factor 3
and tables for storing the user interaction events.

```sh 
CASSANDRA_CTR=$(docker container ls | grep 'cassandra-1' | awk '{print $1}')
docker cp cassandraCQLScript.cql $CASSANDRA_CTR:/
docker exec -it $CASSANDRA_CTR cqlsh -f cassandraCQLScript.cql 
```

Query cassandra via client cqlsh:

```sh
docker-compose exec -it cassandra-1 cqlsh
```

OR directly execute any query:

```sh
docker exec -it $CASSANDRA_CTR cqlsh -e 'SELECT * FROM browse_keyspace.events_count'
```

## Run Presto

Start Presto :

```sh
docker-compose up -d presto-coordinator presto-worker-1 presto-worker-2
```

Copy 'cassandra.properties' to Presto container:

```sh
PRESTO_CTR=$(docker container ls | grep 'presto-coordinator' | awk '{print $1}') 
docker cp ./presto-config/presto-cassandra-config/cassandra.properties $PRESTO_CTR:/opt/presto-server/etc/catalog/cassandra.properties
```

Confirm cassandra.properties was moved to Presto container:

```sh
docker exec -it $PRESTO_CTR sh -c "ls /opt/presto-server/etc/catalog"
```

Confirm Presto CLI can see Cassandra catalog:

1. Start Presto CLI

```sh
docker exec -it $PRESTO_CTR presto-cli
```

2. Run show command

```sh
show catalogs ;
```

If you do not see cassandra, then we need to restart Presto container:

```sh
docker restart $PRESTO_CTR
```

Repeat 1. and 2. and confirm if you can now see the cassandra catalog

Using Presto-CLI:

```sh
docker exec -it $PRESTO_CTR presto-cli
```

Within Presto CLI, run any query:

```sh
SELECT * FROM cassandra.watch_keyspace.events_count;
```

## Run Spark Streaming

```sh
TOPIC=browse
./venv/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 src/spark.py $TOPIC
```

## Run Data Generator

```sh
python src/data_generator.py
```

## Cleanup

```sh
docker compose down
```
