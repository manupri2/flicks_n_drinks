import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
require('../css/fullstack.css');


class LoggingButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {nameVal: "Click me"};
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.setState(state => ({
      nameVal: state.nameVal + "1"
    }));
    ReactDOM.render(<App />, document.getElementById("content"));
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
