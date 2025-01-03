# Django sync or async, that's the question

Test the performance and concurrency processing of a Django view calling an "external" API with the following servers:

- uWSGI (WSGI)
- uWSGI with Gevent (WSGI)
- Gunicorn (gthread) (WSGI)
- Gunicorn with Gevent (WSGI)
- Uvicorn (ASGI)


## View calling an "external" API

We are testing a Django view which will call an "external" API several times.

We'll use the [httpx](https://www.python-httpx.org/) package for this, as it provides both a sync and async API.

The "external" API, which runs locally with `uvicorn` using `asyncio.sleep` to simulate latency selects a random country from a predefined list:

https://github.com/maerteijn/django-sync-or-async/blob/42793ac6f511d42ec7c1c66be008aa6e1af2eef7/src/django_sync_or_async/views.py#L14-L22


## Overview

We will test the performance implications with the following configurations:

```

                         ┌─────────────────────────────┐
    ┌────────────────────┤ uwsgi-2-threads (:8000)     │
    │                    │ (1 process, 2 threads)      │
    │                    └─────────────────────────────┘
    │                    ┌─────────────────────────────┐
    │  ┌─────────────────┤ uwsgi-100-threads (:8001)   │
    │  │                 │ (1 process, 100 threads)    │
    │  │                 └─────────────────────────────┘
    │  │                 ┌─────────────────────────────┐
    ▼  ▼                 │ uwsgi-gevent (:8002)        │
 ┌───────────┐   ┌───────┤ (1 process, 100 "workers")  │
 │API (:5000)│◄──┘       └─────────────────────────────┘
 │ (uvicorn) │◄──┐       ┌─────────────────────────────┐
 └───────────┘   └───────┤ gunicorn-100-threads (:8003)│
    ▲   ▲                │ (1 process, 100 threads)    │
    │   │                └─────────────────────────────┘
    │   │                ┌─────────────────────────────┐
    │   └────────────────┤ gunicorn-gevent (:8004)     │
    │                    │(1 process, 100 "workers")   │
    │                    └─────────────────────────────┘
    │                    ┌─────────────────────────────┐
    └────────────────────┤ uvicorn (:8005)             │
                         │ (1 process)                 │
                         └─────────────────────────────┘

```
### Concurrency

The view which will be benchmarked calls our "really slow" external API three times so we can also test these calls are done in parallel instead of sequential. The slowest response time is around 600ms, so this is about the longest time it takes the API should generate a response because the API calls should be executed in parallel. To achieve this we use a `ThreadPoolExecutor` for the sync view:

https://github.com/maerteijn/django-sync-or-async/blob/42793ac6f511d42ec7c1c66be008aa6e1af2eef7/src/django_sync_or_async/views.py#L25-L38

Note: The standard `ThreadPoolExecutor` with actual threads is used when using threads, and a special variant for gevent is used when we are in `gevent uwsgi` mode. This will be auto-detected:

https://github.com/maerteijn/django-sync-or-async/blob/42793ac6f511d42ec7c1c66be008aa6e1af2eef7/src/django_sync_or_async/threadpool.py#L1-L9

For the `uvicorn` version (ASGI), the parallel calls are implemented with `asyncio.gather`:

https://github.com/maerteijn/django-sync-or-async/blob/42793ac6f511d42ec7c1c66be008aa6e1af2eef7/src/django_sync_or_async/views.py#L41-L56


## Installation

### Requirements

- Python 3.12 (minimum)
- virtualenv (recommended)


### Install the packages

First create a virtualenv in your preferred way, then install all packages with:
```bash
make install
```

## Running the services

Make sure you are allowed to have many file descriptions open:
```bash
ulimit -n 32768
```

Now run the supervisor daemon which will start all services:
```bash
$ supervisord
```

This will start the API and all the different uwsgi / asgi services. Press `ctrl+c` to stop it.


## Run the benchmarks

You can run the benchmarks for each individual server by selecting the relevant port number so comparison can be made after running them:

For `uwsgi`:
```bash
make locust HOST=http://localhost:8000
```

This will start a locust interface, accessible via http://localhost:8089

For `uwsgi-100-threads`:
```bash
make locust HOST=http://localhost:8001
```

Etcetera, see the [port numbers in the overview](#overview).

### uwsgitop

You can see detailed information during the benchmarks for the uWSGI processes using `uwsgitop`:
```bash
uwsgitop http://localhost:3030  # <-- for the 1 process 2 threads variant
uwsgitop http://localhost:3031  # <-- for the 1 process 100 threads variant
uwsgitop http://localhost:3032  # <-- for the 1 process gevent variant
```
