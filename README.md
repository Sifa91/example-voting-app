OpennShift Voting App
=========

A simple distributed application running across multiple Pods.

Getting started
---------------

Make sure you have an OpenShift cluster running


## Deploy the app in OpenShift

First create the vote namespace

```
$ oc new-project vote
```

Run the following command to create the deployments and services objects:
```
$ oc create -f vote-app.yml
deployment "db" created
service "db" created
deployment "redis" created
service "redis" created
deployment "result" created
service "result" created
deployment "vote" created
service "vote" created
deployment "worker" created
```

Architecture
-----

![Architecture diagram](architecture.png)

* A front-end web app in [Python](/vote) which lets you vote between two options
* A [Redis](https://hub.docker.com/_/redis/) queue which collects new votes
* A [Java](/worker/src/main) or [.NET Core 2.1](/worker/dotnet) worker which consumes votes and stores them in…
* A [Postgres](https://hub.docker.com/_/postgres/) database backed by a Persistent volume
* A [Node.js](/result) webapp which shows the results of the voting in real time


Note
----

The voting application only accepts one vote per client. It does not register votes if a vote has already been submitted from a client.
