# django-traffic
A Django middleware that helps visualize your app's traffic in Kibana

In a nutshell, by using this middleware you need no more effort to stream your app's traffic in your
ElasticSearch host(s) and use Kibana for visualizations around it.
The first version of this lib handles map tiles in Kibana, so you can see on the map where's your traffic coming from.

Geolocation is achieved by using `django.contrib.gis.geoip2.GeoIP2` wrapper, included in Django 1.9 and latter.

# Quick Start
  **1. Install using pip:**

  ```
  pip install django-traffic
  ```

  ** 2. Include "django-traffic" in your INSTALLED_APPS:**

  ```
  INSTALLED_APPS = [
      ...
      'django-traffic',
  ]
  ```

  **3. Include "ESTrafficInfoMiddleware" to your MIDDLEWARE_CLASSES:**

  ```
  MIDDLEWARE_CLASSES = (
      ...
      'django-traffic.middleware.ESTrafficInfoMiddleware',
  )
  ```
# Configuration
There are some variables required in your `settings.py` file to function normally.
- `TRAFFIC_INDEX_NAME`: this is the name of the index that will be used in ElasticSearch.
 If you leave this empty or do not define it, the default index name will be applied: `django-traffic`.

- `ES_CLIENT`: if you already have an ElasticSearch() client instance ready in your app, we'll use this one be default.

- `ES_HOST`: this is required only if you don't have an `ES_CLIENT` defined. Here the lib expects to find a hostname
(including the port) of your ElasticSearch instance.

- `GEO_DB_PATH`: if you don't have `GEOIP_PATH` already defined, you need to define the path where django can find your
geolocation database.

After you deploy your project or locally run your django server, requests and traffic to your web app will be sent to
the ElasticSearch hosts defined. Practically you are ready to create a Kibana map-tile visualization and start watching
where traffic is flooding you in.

# Contributing - Error Reporting
This lib was made with my own needs in mind, so it's uncommon to fit everyone's project out there.
For Error Reporting, open an issue in Github and I will try to take care of it as soon as possible.
If you are able to contribute to this lib and make it better, feel free to fork it and adjust it to your use-case.

