
# opendir-dl-web

This is a simple read only web frontend for the [opendir-dl](https://github.com/bplower/opendir-dl) project. It is just a Flask application that executes keyword searches on items in the default database.

For testing and development, you can run the source via `make run`. An example is as follows:

```
virtualenv venv
source venv/bin/activate
git clone https://github.com/bplower/opendir-dl-web.git
cd opendir-dl-web
pip install git+https://github.com/bplower/opendir-dl.git
make install
make run
```

## Example files
There are example files for hosting this on apache with wsgi
* examples/example_apache2_opendir-dl-web.conf
* examples/example_wsgi-opendir-dl-web.wsgi
