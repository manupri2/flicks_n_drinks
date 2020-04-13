import React from 'react';
import { Row, Form, Col, Button } from 'react-bootstrap';

class AddCocktail extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
      recipeId: '',
      cocktailName: 'Test',
    }

    if(props.item){
      this.state = props.item
    } else {
      this.state = this.initialState;
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    
    this.setState({
      [name]: value
    })

  }

  handleSubmit(event) {
    event.preventDefault();
    this.props.onFormSubmit(this.state);
    this.setState(this.initialState);
  }

  render() {

    let pageTitle;
    if(this.state.recipeId>=0) {
      pageTitle = <h2>Edit Cocktail</h2>
    } else {
      pageTitle = <h2>Add Cocktail</h2>
    }

    return(
      <div>
        {pageTitle}
        <Row>
          <Col sm={6}>
            <Form onSubmit={this.handleSubmit}>
              <Form.Group controlId="cocktailName">
                <Form.Label>Cocktail Name</Form.Label>
                <Form.Control
                  type="text"
                  name="cocktailName"
                  value={this.state.cocktailName}
                  onChange={this.handleChange}
                  placeholder=""/>
              </Form.Group>
              <Form.Group>
                <Form.Control type="hidden" name="recipeId" value={this.state.recipeId} />
                <Button variant="success" type="submit">Save</Button>
              </Form.Group>
            </Form>
          </Col>
        </Row>
      </div>
    )
  }
}

export default AddCocktail;
