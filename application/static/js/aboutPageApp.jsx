import React from "react";
import ReactDOM from "react-dom";
require('../css/fullstack.css');


function TestRender(props){
		var error1 = props.elems.error;
		var isLoaded = props.elems.isLoaded;
		var items = props.elems.items;
		var table = props.elems.table;
		var base_query = props.elems.base_query;



        fetch(base_query + table)
            .then(res => res.json())
            .then(
                    (result) => {
                            isLoaded = true;
                            items = result.data;
                    },
                    (error) => {
                            isLoaded = true;
                            error1 = error;
                    }
            )



		if(error1){
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


class QueryApp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
                nameVal: "Click mee",
                error: null,
                isLoaded: false,
                items:[],
                table: '',
                base_query: 'http://cs411ccsquad.web.illinois.edu/api/SELECT%20%2A%20FROM%20',
            };
        // This binding is necessary to make `this` work in the callback
        this.handleClick = this.handleClick.bind(this);
    }


    handleClick() {
        var text_val = document.getElementById("table").value;

        this.setState(state => ({
          nameVal: state.nameVal + text_val,
          table: text_val,
          isLoaded: false,
          error: null
        }));

        this.test_Query();
    }


    test_Query() {

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


    render() {
        return (
          <div>
            <button onClick={() => this.handleClick()}>
            {this.state.nameVal}
            </button>
           <TestRender elems={this.state} />
          </div>
        );
    }
}


export default QueryApp;
