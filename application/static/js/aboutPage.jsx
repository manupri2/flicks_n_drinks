import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
require('../css/fullstack.css');

function validateForm() {
  document.getElementById('my_button').value += "1";
  if (x == "") {
    alert("Table name must be filled out!!");
    return false;
  }
  else{
       ReactDOM.render(<App />, document.getElementById("content"));
  }
}
