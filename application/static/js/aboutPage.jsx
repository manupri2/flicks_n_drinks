import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
require('../css/fullstack.css');


function queryMeTimbers(table){
    	var q_str = 'http://cs411ccsquad.web.illinois.edu/api/SELECT%20%2A%20FROM%20';
		q_str += table;

        var dstuff = fetch(q_str).then(res => res.json()).then((result) => {result.data;});

        return q_str;
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
    document.getElementById("content").innerHTML = queryMeTimbers(text_val);
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
