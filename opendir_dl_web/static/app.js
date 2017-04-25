
class SearchResultDisplay extends React.Component {
  render() {
    var results_start = (this.props.data.page - 1) * this.props.data.results_per_page + 1;
    var results_end = (this.props.data.page - 1) * this.props.data.results_per_page + this.props.data.results.length;
    var paragraph_text = "Showing results " + results_start + " through " + results_end + " of " + this.props.data.results_total + " for '" + this.props.data.query + "'";
    return <div><p>{paragraph_text}</p></div>;
  }
}

class SearchResults extends React.Component {
  render() {
    return (
      <div>
        {this.props.data.results.map(item => (
        <div>
          <h4><a href="{item.url}"> {item.name} </a></h4>
          <p>
            <strong>Content Size:</strong> {item.content_length} <br/>
            <strong>Content Type:</strong> {item.content_type} <br/>
            <strong>Last Modified:</strong> {item.last_modified}
          </p>
          <hr/>
        </div>
        ))}
      </div>
    );
  }
}

class Paginator extends React.Component {
  constructor(props) {
    super(props);
    this.calculate_buttons = this.calculate_buttons.bind(this);
    this.get_uri = this.get_uri.bind(this);
    this.state = {
      current_page: this.props.data.page,
      num_pages: this.props.data.num_pages,
      enable_button_step: true,
      enable_button_jump: true,
      num_buttons: 11
    };
  }

  get_uri(page) {
    return "/results?q=" + this.props.data.query + "&page=" + page
  }

  calculate_buttons() {
    var num_navigation_buttons = 2 * (this.state.enable_button_jump + this.state.enable_button_step);
    var num_page_buttons = this.state.num_buttons - num_navigation_buttons;

    if (num_page_buttons > this.state.num_pages) {
      num_page_buttons = this.state.num_pages;
    }
    var current_page_position = Math.ceil(num_page_buttons/2.0);
    if (this.state.current_page < current_page_position) {
      // Check for begining page postion
      current_page_position = this.state.current_page;
    }
    else if (this.state.current_page > this.state.num_pages - current_page_position) {
      // Check for end page position
      current_page_position = num_page_buttons - (this.state.num_pages - this.state.current_page);
    }
    var value_start_range = this.state.current_page - current_page_position + 1;
    var value_page_range = [];
    //for i in range(value_start_range, value_start_range + num_page_buttons) {
    for (var i = value_start_range; i < value_start_range + num_page_buttons; i++) {
      if (this.state.current_page==i) {
        value_page_range.push({classes: "active", display_value: i, uri: this.get_uri(i)});
      }
      else {
        value_page_range.push({classes: "", display_value: i, uri: this.get_uri(i)});
      }
      //value_page_range.push('<a class="btn btn-primary" style="width: 45px" href="/results?q={ query }&page={i}">{i}</a>');
    }

    // Make step buttons if enabled
    if (this.state.enable_button_step) {
      // next button
      if (this.state.current_page == this.state.num_pages) {
        // This means we can't step down a page. Disable the button
        value_page_range.push({classes: "disabled", display_value: ">", uri: this.get_uri(this.state.current_page)})
      } else {
        value_page_range.push({classes: "", display_value: ">", uri: this.get_uri(this.state.current_page + 1)})
      }

      // prev button
      if (this.state.current_page == 1) {
        // This means we can't step down a page. Disable the button
        value_page_range.splice(0, 0, {classes: "disabled", display_value: "<", uri: this.get_uri(this.state.current_page)})
      } else {
        value_page_range.splice(0, 0, {classes: "", display_value: "<", uri: this.get_uri(this.state.current_page - 1)})
      }
    }

    // Make jump buttons if enabled
    if (this.state.enable_button_jump) {
      // last button
      if (this.state.current_page == this.state.num_pages) {
        // This means we can't step down a page. Disable the button
        value_page_range.push({classes: "disabled", display_value: ">>", uri: this.get_uri(1)})
      } else {
        value_page_range.push({classes: "", display_value: ">>", uri: this.get_uri(this.state.num_pages)})
      }

      // first button
      if (this.state.current_page == 1) {
        // This means we can't step down a page. Disable the button
        value_page_range.splice(0, 0, {classes: "disabled", display_value: "<<", uri: this.get_uri(1)})
      } else {
        value_page_range.splice(0, 0, {classes: "", display_value: "<<", uri: this.get_uri(1)})
      }
    }
    return value_page_range;
  }

  render() {
    return (
      <div>
      <ul className="pagination">
      {this.calculate_buttons().map(button => (
        //<a class="btn btn-primary" style="width: 45px" href="/results?q={ query }&page={button.page_num}">{button.page_num}</a>
        // <li className={button.classes}><a style={{width: 45}} href={button.uri}>{button.display_value}</a></li>
        <li className={button.classes}><a href={button.uri}>{button.display_value}</a></li>
      ))}
      </ul>
      </div>
    );
  }
}

// <div style="text-align: center; margin: 20px">
// {% for button in paginator.render_list() %}
//   {% if button.type == "page" and button.number == paginator.current_page %}
//   <a class="btn btn-primary" style="width: 45px" href="/results?q={{ query }}&page={{ button.number }}" disabled>{{ button.value }}</a>
//   {% elif button.type == "jump" or button.type == "step" %}
//   <a class="btn btn-default" href="/results?q={{ query }}&page={{ button.number }}">{{ button.value }}</a>
//   {% else %}
//   <a class="btn btn-primary" style="width: 45px" href="/results?q={{ query }}&page={{ button.number }}">{{ button.value }}</a>
//   {% endif %}
// {% endfor %}
// </div>

function get_param(name){
  // Retrieve the value for a variable defined by 'name'
  if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}
