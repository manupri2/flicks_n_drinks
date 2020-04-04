import React, {Component} from "react";
import '../css/fullstack.css'


class App extends Component{
	
	constructor(props) {
		super(props);
		
		this.state = {
			error: null,
			isLoaded: false,
			items:[]
		};
	}
	
	componentDidMount(){
		fetch('http://cs411ccsquad.web.illinois.edu/oscar-testing/api/SELECT%20%2A%20FROM%20CocktailName')
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
			return <div>Loading here...</div>;
		} else{
			return(
				<div>Results!!</div>
			);
		}
	}
}


export default App;
