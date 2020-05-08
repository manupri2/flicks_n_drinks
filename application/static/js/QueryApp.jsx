import React from "react";


function QueryResults(props){
    const error = props.data.error;
    const isLoaded = props.data.isLoaded;
    const items = props.data.items;
    const table = props.data.table;
    const base_query = props.data.base_query;

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
                        {JSON.stringify(item)}
                    </li>
                ))}
            </ul>
        );
    }
}


class TestApp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
                nameVal: "Submit Query",
                table: '',
                error: null,
                isLoaded: false,
                items:[],
                base_query: 'http://cs411ccsquad.web.illinois.edu/',
         };
        // This binding is necessary to make `this` work in the callback
        this.handleClick = this.handleClick.bind(this);
        this.test_Query = this.test_Query.bind(this);
    }


    handleClick() {
        var text_val = document.getElementById("table").value;
        this.setState(state => ({
          table: text_val,
          error: null,
          isLoaded: false,
        }));
    }


    test_Query(){
            if(!this.state.isLoaded){
                fetch(this.state.base_query + this.state.table)
                    .then(res => res.json())
                    .then(
                        (result) => {
                            this.setState({
                                isLoaded: true,
                                items: result.data,
                                error: null
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
    }


    render() {
        this.test_Query();

        return (
            <div>
            <button onClick={() => this.handleClick()}>
            {this.state.nameVal}
            </button>
            <QueryResults data={this.state} />
            </div>
        );
    }
}


export default TestApp;
