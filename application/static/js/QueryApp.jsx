import React from "react";
import ReactDOM from "react-dom";
require('../css/fullstack.css');


class QueryApp extends React.Component {

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
        const new_table = this.props.table
        fetch(this.state.base_query + new_table)
			.then(res => res.json())
			.then(
				(result) => {
					this.setState({
						isLoaded: true,
						items: result.data,
						table: new_table,
						error: null
					});
				},
				(error) => {
					this.setState({
						isLoaded: true,
						table: new_table,
						error
					});
				}
			)
    }


	componentDidMount(){
	    this.test_Query();
	}


	render(){
		const {error, isLoaded, items, table, base_query} = this.state;

		if(table == ''){
		    return <div>Please enter a table name.</div>;
		} else if(error){
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

export default QueryApp;
