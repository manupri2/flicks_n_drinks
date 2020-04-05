import React from "react";
import ReactDOM from "react-dom";
require('../css/fullstack.css');


class Display extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			error: null,
			isLoaded: false,
			items:[],
			table: this.props.table,
			base_query: 'http://cs411ccsquad.web.illinois.edu/api/SELECT%20%2A%20FROM%20',
		};
		this.test_Query = this.test_Query.bind(this);
	}

    test_Query(){
        this.setState({
						table: this.props.table,
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

	componentDidMount(props){
	    this.test_Query();
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

export default Display;
