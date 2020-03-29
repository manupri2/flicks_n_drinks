function getmore(text) {
  var bool = confirm("Are you sure you want " + text);
  get_more_alert(text, bool);
}

function get_more_alert(text, bool) {
  if (bool) {
    alert(eatit(text) + ' biiaaaatch!!');
  } else {
    alert('No ' + text + ' biiaaaatch!!');
  }
  var elem = text + "Div"
  document.getElementById(elem).innerHTML += "1";
}

function eatit(text) {
  return text + " eat it!!";
}

function change_text(){
  var dd1 = document.getElementById('pudge');
  dd1.innerHTML += " It is very delicious!";
}

function change_color(){
  var dd1 = document.getElementById('pudge');
  dd1.style.color = "red";
}

function change_class(){
  var dd1 = document.getElementById('pudge');
  dd1.className = "divChangeClass";
}

function remove_class(){
  var dd1 = document.getElementById('pudge');
  dd1.className = "";
}

function change_butt_val(){
  var dd1 = document.getElementById('butt1');
  dd1.value += "1";
}

function changeColor(){
  var dd1 = document.getElementById('canvas1');
  var dd2 = document.getElementById('canvas2');
  dd1.style.backgroundColor = "red";
  dd2.style.backgroundColor = "blue";
}

function addElements() {
  var dd1 = document.getElementById('canvas1');
  var dd2 = document.getElementById('canvas2');
  var elems = [dd1, dd2];
  var dd;
  
  for (dd of elems) {
    var ctx = dd.getContext("2d");
    ctx.fillStyle = "black";
    ctx.fillRect(10,10,40,40);
    ctx.font = "30px Arial";
    ctx.fillText('Hello',20,80);
  }
}

function clear_the_rect() {
  var dd1 = document.getElementById('canvas1');
  var ctx = dd1.getContext("2d");
  ctx.clearRect(10,10,40,40);
}