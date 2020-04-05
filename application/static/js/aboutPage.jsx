import React from "react";
import ReactDOM from "react-dom";
require('../css/fullstack.css');

function validateForm() {
  var x = document.forms["myForm"]["table"].value;
  if (x == "") {
    alert("Table name must be filled out!!");
    return false;
  }
}
