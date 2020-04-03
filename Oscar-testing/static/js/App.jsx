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
		fetch('http://localhost:4000/Bars')
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
						<li key={item.id}>
							Bar: {item.name} 
							{/* <span style="margin-left:2em">Address: {item.address}</span> */}
							{/* <span style="margin-left:2em">Address: {item.owner}</span> */}
						</li>
					))}
				</ul>
			);
		}
	}
}


export default App;
