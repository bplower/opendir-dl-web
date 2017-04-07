import math
import json
from flask import Flask
from flask import request
from flask import current_app
from flask import render_template
from flask import send_from_directory
import opendir_dl

class Pagination(object):
    def __init__(self):
        self.current_page = 0
        self.total_pages = 10
        self.enable_button_step = False
        self.enable_button_jump = True
        self.num_buttons = 5

        if not self.enable_button_step and not self.enable_button_jump and self.total_pages < 5:
            raise ValueError("Enabling step and jump buttons requires 5 or more total buttons. Currently {}".format(self.num_buttons))
        if (not self.enable_button_step or not self.enable_button_jump) and self.total_pages < 3:
            raise ValueError("Enabling step or jump buttons requires 3 or more total buttons. Currently {}".format(self.num_buttons))

    def displayed_page_numbers(self):
        num_navigation_buttons = 2 * sum([self.enable_button_jump, self.enable_button_step])
        num_page_buttons = self.num_buttons - num_navigation_buttons
        if num_page_buttons > self.total_pages:
            num_page_buttons = self.total_pages
        current_page_position = int(math.ceil(num_page_buttons/2.0))
        if self.current_page < current_page_position:
            # Check for begining page postion
            current_page_position = self.current_page
        elif self.current_page > self.total_pages - current_page_position:
            # Check for end page position
            current_page_position = num_page_buttons - (self.total_pages - self.current_page)
        value_start_range = self.current_page - current_page_position + 1
        value_page_range = []
        for i in range(value_start_range, value_start_range + num_page_buttons):
            value_page_range.append({"type": "page", "number": i, "value": str(i)})
        return value_page_range

    def render_list(self):
        value_range = self.displayed_page_numbers()
        if self.enable_button_step:
            value_range.insert(0, {"type": "step", "number": self.current_page - 1, "value": "<"})
            value_range.append({"type": "step", "number": self.current_page + 1, "value": ">"})
        if self.enable_button_jump:
            value_range.insert(0, {"type": "jump", "number": 1, "value": "<<"})
            value_range.append({"type": "jump", "number": self.total_pages, "value": ">>"})
        return value_range

    def print_range(self):
        for i in self.render_list():
            print i

class WebSearchCommand(opendir_dl.commands.BaseCommand):
    valid_options = []
    valid_flags = []

    def run(self):
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
        self.config.update(TEMPLATES_AUTO_RELOAD=True)
        self.debug = True

        # Register our routes
        self.route("/")(self.page_index)
        self.route("/results")(self.page_results)
        self.route("/static/<path:path>")(self.serve_static)
        self.route("/api/search", methods=['POST'])(self.api_search)

    def serve_static(self, path):
        return send_from_directory('static', path)

    def page_index(self):
        return self.serve_static('index.html')

    def page_results(self):
        return self.serve_static('results.html')

    def api_search(self):
        results_per_page = 20
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
            'pages': num_pages,
            'results_per_page': results_per_page,
            'results_total': len(results),
            'results': result_list
        }
        return json.dumps(return_dict)

    def results(self):
        results_per_page = 20
        page = int(request.args.get('page', 1))
        query = request.args.get('q', '')
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
            displayed_results = results[start_index: end_index]
        else:
            displayed_results = results
        num_pages = int(math.ceil(float(len(results))/results_per_page))
        # Build and configure the pagination tracker
        pages = Pagination()
        pages.enable_button_step = True
        pages.current_page = page
        pages.total_pages = num_pages
        pages.num_buttons = 11
        # Now render and return the page
        return render_template('search.html',
            paginator = pages,
            results=displayed_results,
            num_results_per_page=results_per_page,
            num_total_results=len(results),
            query=query)

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
    app.run(host = host, port = port)
