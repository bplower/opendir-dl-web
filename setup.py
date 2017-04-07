from setuptools import setup

setup(
    # Application name:
    name = "opendir_dl_web",

    # Version number:
    version = "0.0.0",

    # Application author details:
    author = "Brahm Lower",
    author_email = "bplower@gmail.com",

    # License
    license = "",

    # Packages:
    packages = ["opendir_dl_web"],

    package_data = {
        "opendir_dl_web": [
            "static/index.html",
            "static/results.html",
            "static/app.js"
        ]
    },

    data_files = [
        ('/var/www/opendir-dl-web/', ['examples/example_wsgi-opendir-dl-web.wsgi'])
    ],

    # Details:
    url = "https://github.com/bplower/opendir-dl-web",

    # Description:
    description = "This is a simple web frontend for opendir-dl.",

    # Dependant packages:
    install_requires = [
        "flask",
        "opendir-dl"
    ],
)
