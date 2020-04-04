import React from "react";
import ReactDOM from "react-dom";
require('../css/fullstack.css');


function validateForm() {
  var x = document.forms["myForm"]["table"].value;
  if (x == "") {
    alert("Please enter a table name!");
    return false;
  }
}
