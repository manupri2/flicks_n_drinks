import React from 'react';
import { Table, Button, Alert, Spinner } from 'react-bootstrap';

class CocktailList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        response: {}
    }
  }

  render() {
    const error = this.props.info.error;
    const cocktails = this.props.info.items;
    const isLoaded = this.props.info.isLoaded;
    const query = this.props.info.query;

    if(error) {
      return (
        <div>Request: {query}</div>
      )
    } else if(!isLoaded) {
      return (<div><Spinner animation="grow" /></div>)
    } else {
      return(
        <div>
          <h2>Cocktail List</h2>
          {this.state.response.message && <Alert variant="info">{this.state.response.message}</Alert>}
          <Table>
            <thead>
              <tr>
                <th>Cocktail Name</th>
                <th>Ingredients</th>
                <th>Bartender</th>
                <th>Location</th>
                <th>Glassware</th>
                <th>Rating</th>
                <th>Edit/Delete</th>
              </tr>
            </thead>
            <tbody>
              {cocktails.map(cocktail => (
                <tr key={cocktail.recipeId}>
                  <td>{cocktail.cocktailName}</td>
                  <td>{cocktail.ingredients}</td>
                  <td>{cocktail.bartender}</td>
                  <td>{cocktail.location}</td>
                  <td>{cocktail.glasswareName}</td>
                  <td>{cocktail.rating}</td>
                  <td>
                    <Button variant="info" onClick={() => this.props.editItem(cocktail.recipeId)}>Edit</Button>
                    &nbsp;<Button variant="danger" onClick={() => this.props.deleteItem(cocktail.recipeId)}>Delete</Button>
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

export default CocktailList;
