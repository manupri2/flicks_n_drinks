import React from 'react';
import { Table, Button, Alert } from 'react-bootstrap';


class ProductList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      products: [],
      response: {}
    }
  }

  componentDidMount() {
    // const apiUrl = 'http://127.0.0.1:5000/CocktailName';
    const apiUrl = 'http://cs411ccsquad.web.illinois.edu/CocktailName';

    fetch(apiUrl)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            products: result.data
          });
        },
        (error) => {
          this.setState({ error });
        }
      )
  }

  deleteProduct(productId) {
    const { products } = this.state;

    const arrayCopy = this.state.products.filter((row) => row.cocktailId != productId);
    this.setState({products:arrayCopy});

    // const apiUrl = 'http://localhost:5000/delete';
    const apiUrl = 'http://cs411ccsquad.web.illinois.edu/delete';

    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({product_id:productId})
    }
    
     fetch(apiUrl, options)
 
 }


  render() {
    const {error, products} =this.state;

    if(error) {
      return (
        <div>Error: {error.message}</div>
      )
    } else {
      return(

        <div>
          <h2>Product List</h2>
          {this.state.response.message && <Alert variant="info">{this.state.response.message}</Alert>}
          <Table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Cocktail Name</th>
              </tr>
            </thead>
            <tbody>
              {products.map(product => (
                <tr key={product.cocktailId}>
                  <td>{product.cocktailId}</td>
                  <td>{product.cocktailName}</td>
                  <td>
                    <Button variant="info" onClick={() => this.props.editProduct(product.cocktailId)}>Edit</Button>
                    &nbsp;<Button variant="danger" onClick={() => this.deleteProduct(product.cocktailId)}>Delete</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      )
    }
  }
}

export default ProductList;
