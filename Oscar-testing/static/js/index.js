const express = require('express');
const cors= require('cors');
const mysql = require('mysql');

const app = express();

const SELECT_ALL_BARS_QUERY = 'SELECT * FROM Bars';

const connection = mysql.createConnection({
  host:'localhost',
  user: 'root',
  password: 'cj;6qup3vu;6',
  database: 'MP1'
});

connection.connect(err => {
  if(err){
    return err;
  }
});

app.use(cors());

app.get('/', (req,res) => {
  res.send('go to /producs to see products')
});

app.get('/items/add', (req,res) =>{
  const {id, name, price} = req.query;
  console.log(id, name, price);
  const INSERT_BARS_QUERY = `INSERT INTO Item (id, name, price) VALUES('${id}','${name}','${price}')`
  connection.query(INSERT_BARS_QUERY, (err, results)=>{
    if(err){
      return res.send(err)
    }
    else{
      return res.send('Successfullt added product')
    }
  });
});

app.get('/Bars', (req,res) =>{
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

app.listen(4000, () =>{
  console.log('MP1 server listening on port 4000')
});
