climata-viewer
==============

Interactive database and analysis tools for the [climata] library.  Powered by [wq] and [Django REST Pandas].

Live Demo: <http://climata.houstoneng.net>

## Installation

Follow the instructions on <http://wq.io/docs/setup>, but replace

```bash
wq-start $PROJECTNAME
```

with

```bash
git clone https://github.com/heigeo/climata-viewer.git $PROJECTNAME
```

## Configuration

Log into the Django administrative interface and create a new Webservice pointing to one of the climata IO classes.

[climata]: https://github.com/heigeo/climata
[wq]: http://wq.io/
[Django REST Pandas]: https://github.com/wq/django-rest-pandas
