import React from "react";
import ReactDOM from "react-dom";
require('../css/fullstack.css');


class Query extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			error: null,
			isLoaded: false,
			items:[],
			table: '',
			base_query: 'http://cs411ccsquad.web.illinois.edu/api/SELECT%20%2A%20FROM%20',
		};
		this.test_Query = this.test_Query.bind(this);
	}

    test_Query(){
        this.setState({
						table: document.getElementById("table").value,
					});
        fetch(this.state.base_query + this.state.table)
			.then(res => res.json())
			.then(
				(result) => {
					this.setState({
						isLoaded: true,
						items: result.data
					});
				},
				(error) => {
					this.setState({
						isLoaded: true,
						error
					});
				}
			)
    }

	componentDidMount(){
	this.timerID = setInterval(() => this.test_Query(), 5000);
	}


	render(){
		const {error, isLoaded, items, table, base_query} = this.state;
		if(error){
			return <div>Error, bad query: {base_query + table} </div>;
		} else if(!isLoaded){
			return <div>Loading...</div>;
		} else{
			return(
				<ul>
					{items.map(item =>(
						<li>
							{item.cocktailName}
						</li>
					))}
				</ul>
			);
		}
	}
}


class LoggingButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {nameVal: "Click mee"};
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    var text_val = document.getElementById("table").value;

    this.setState(state => ({
      nameVal: state.nameVal + text_val
    }));

  }

  render() {
    // This syntax ensures `this` is bound within handleClick
    return (
      <button onClick={() => this.handleClick()}>
        {this.state.nameVal}
      </button>
    );
  }
}

ReactDOM.render(<LoggingButton />, document.getElementById("my_button"));
ReactDOM.render(<Query />, document.getElementById("content"));