import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
require('../css/fullstack.css');


function validateForm() {
  document.getElementById('my_button').value += "1";
  ReactDOM.render(<App />, document.getElementById("content"));
}
