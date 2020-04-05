import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
require('../css/fullstack.css');


class LoggingButton extends React.Component {
  handleClick() {
    this.value += "1";
  }

  render() {
    // This syntax ensures `this` is bound within handleClick
    return (
      <button onClick={() => this.handleClick()}>
        Click me query!
      </button>
    );
  }
}

ReactDOM.render(<LoggingButton />, document.getElementById("my_button"));
