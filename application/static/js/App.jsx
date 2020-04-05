import React, {Component} from "react";
import '../css/fullstack.css'


class App extends Component{
	
	constructor(props) {
		super(props);
		
		this.state = {
			error: null,
			isLoaded: false,
			items:[],
			query: 'http://cs411ccsquad.web.illinois.edu/api/SELECT%20%2A%20FROM%20' + document.getElementById("table").value
		};
	}
	
	componentDidMount(){
		fetch(this.state.query)
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


	render(){
		const {error, isLoaded, items} = this.state;
		if(error){
			return <div>Error: {error.message} </div>;
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


export default App;

