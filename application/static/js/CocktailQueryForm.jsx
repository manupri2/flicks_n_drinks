import React from 'react';
import { Row, Form, Col, Button } from 'react-bootstrap';


class CocktailQueryForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          cocktailName: {value: '', operator: 'LIKE'} ,
          ingredients: {value: '', operator: 'LIKE'},
          bartender: {value: '', operator: 'LIKE'},
          location: {value: '', operator: 'LIKE'},
          rating: {value: '', operator: '>='}
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

  handleSubmit(event) {
    event.preventDefault();
    this.props.updateFilters(this.state);
    // this.setState(this.initialState);
  }

  handleChange(event) {
    const name = event.target.name;
    const new_value = event.target.value;
    const old_operator = this.state.[name].operator;

    this.setState({
      [name]: {value: new_value, operator: old_operator}
    });
  }

    render() {

          return(
              <Form onSubmit={this.handleSubmit}>
                  <Row>
                      <Col>
                          <Form.Row>
                                <Form.Group controlId="CocktailName">
                                  <Form.Label>Cocktail Name:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="cocktailName"
                                        value={this.state.cocktailName.value}
                                        onChange={this.handleChange}
                                        placeholder="Enter cocktail name" />
                                </Form.Group>

                                <Form.Group controlId="Ingredients">
                                  <Form.Label>Ingredients:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="ingredients"
                                        value={this.state.ingredients.value}
                                        onChange={this.handleChange}
                                        placeholder="Enter ingredients" />
                                </Form.Group>

                                <Form.Group controlId="Bartender">
                                  <Form.Label>Bartender:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="bartender"
                                        value={this.state.bartender.value}
                                        onChange={this.handleChange}
                                        placeholder="Enter bartender" />
                                </Form.Group>

                                <Form.Group controlId="Location">
                                  <Form.Label>Location:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="location"
                                        value={this.state.location.value}
                                        onChange={this.handleChange}
                                        placeholder="Enter location" />
                                </Form.Group>

                                <Form.Group controlId="Rating">
                                  <Form.Label>Rating:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="rating"
                                        value={this.state.rating}
                                        onChange={this.handleChange}
                                        placeholder="1-10" />
                                </Form.Group>
                          </Form.Row>
                      </Col>
                       <Button className="h-25" variant="success" type="submit">Submit</Button>
                  </Row>
              </Form>
          )
    }
}

export default CocktailQueryForm;