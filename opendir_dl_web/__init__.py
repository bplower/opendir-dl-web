import math
import json
from flask import Flask
from flask import request
from flask import current_app
from flask import render_template
from flask import send_from_directory
import opendir_dl

@opendir_dl.commands.BaseCommand.factory
def WebSearchCommand(self):
    # Prepare the database connection
    if not self.db_connected():
        self.db_connect()
    # Execute the query
    search = opendir_dl.utils.SearchEngine(self.db_wrapper.db_conn, self.values)
    search.exclusive = self.has_flag("inclusive")
    return search.query()

class OpendirDlWeb(Flask):
    def __init__(self, *args, **kwargs):
        # Prepare the config path for the the opendir_dl instance
        config_filepath = kwargs.pop("config_filepath", None)
        if not config_filepath:
            config_filepath = opendir_dl.get_config_path("config.yml")
        self.opendirdl_config = opendir_dl.Configuration(config_path=config_filepath)

        # Call the superclass
        super(OpendirDlWeb, self).__init__(*args, **kwargs)

        # Following two lines are used for debugging
        # self.config.update(TEMPLATES_AUTO_RELOAD=True)
        # self.debug = True

        # Register our routes
        self.route("/")(self.page_index)
        self.route("/results")(self.page_results)
        self.route("/static/<path:path>")(self.serve_static)
        self.route("/api/search", methods=['POST'])(self.api_search)

    def serve_static(self, path):
        """
        Serves static files from the 'static' folder within the python package
        """
        return send_from_directory('static', path)

    def page_index(self):
        """
        Gets the index page
        """
        return self.serve_static('index.html')

    def page_results(self):
        """
        Gets the results pages
        """
        return self.serve_static('results.html')

    def api_search(self):
        """
        Executes a query and provides the results for the page currently being
        displayed. Currently gets all results of the query from the database
        and then selects the subsection of the returned items
        """
        results_per_page = 20
        if request.form.get('page') == 'undefined':
            page = 1
        else:
            page = int(request.form.get('page', 1))
        query = request.form.get('q', '')
        # Handle user input
        input_values = query.split(' ')
        # Prepare the search command and execute the search
        command_instance = WebSearchCommand()
        command_instance.config = self.opendirdl_config
        command_instance.flags = ["inclusive"]
        command_instance.values = input_values
        results = command_instance.run()
        if len(results) > results_per_page:
            start_index = (page - 1) * results_per_page
            end_index = start_index + results_per_page
            raw_results = results[start_index: end_index]
        else:
            raw_results = results
        num_pages = int(math.ceil(float(len(results))/results_per_page))

        # Make clean dicts out of our raw_results
        result_list = []
        for i in raw_results:
            result_list.append({
                'name': i.name,
                'url': i.url,
                'content_length': i.content_length,
                'content_type': i.content_type,
                'last_modified': str(i.last_modified)
            })
        return_dict = {
            'query': query,
            'page': page,
            'num_pages': num_pages,
            'results_per_page': results_per_page,
            'results_total': len(results),
            'results': result_list
        }
        return json.dumps(return_dict)

def main(arg_list):
    try:
        host = arg_list[0]
    except IndexError:
        host = '0.0.0.0'

    try:
        port = arg_list[1]
    except IndexError:
        port = 8000

    app = OpendirDlWeb("opendir_dl_web")
    app.run(host=host, port=port)
