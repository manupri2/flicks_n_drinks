const express = require('express');
const cors= require('cors');
const mysql = require('mysql');

const app = express();

const SELECT_ALL_BARS_QUERY = 'SELECT * FROM CocktailName';


const connection = mysql.createConnection({
  host:'localhost',
  user: 'cs411ccsquad_admin',
  password: 'password;uiuc',
  database: 'cs411ccsquad_FlicksNDrinks'
});


connection.connect(err => {
  if(err){
    return err;
  }
});


app.use(cors());


app.get('/', (req,res) => {
  res.send('go to /Cocktail to see basic query of all Cocktail names')
});


//app.get('/items/add', (req,res) =>{
//  const {id, name, price} = req.query;
//  console.log(id, name, price);
//  const INSERT_BARS_QUERY = `INSERT INTO Item (id, name, price) VALUES('${id}','${name}','${price}')`
//  connection.query(INSERT_BARS_QUERY, (err, results)=>{
//    if(err){
//      return res.send(err)
//    }
//    else{
//      return res.send('Successfullt added product')
//    }
//  });
//});


app.get('/Cocktail', (req,res) =>{
  connection.query(SELECT_ALL_BARS_QUERY,(err,results)=>{
    if(err){
      return res.send(err)
    }
    else{
      return res.json({
        data:results
      })
    }
  });
});


app.listen(3306, () =>{
  console.log('Flicks_n_Drinks server listening on port 3306')
});