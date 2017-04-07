
class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.results = [{result_name: 'testing!!'}]
  }
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
