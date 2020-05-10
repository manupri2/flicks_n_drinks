import React from 'react';
import { Row, Form, Col, Button } from 'react-bootstrap';

class AddCocktail extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
      recipeId: '',
      cocktailName: '',
      bartender: '',
      location: '',
      glasswareName: '',
      isAdd: props.isAdd
    }

    if(props.isAdd){
      this.state = this.initialState;
    } else {
      this.state = {
                      recipeId: props.item.recipeId,
                      cocktailName: props.item.cocktailName,
                      bartender: props.item.bartender,
                      location: props.item.location,
                      glasswareName: props.item.glasswareName,
                      isAdd: false
                    };
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

    var submit_data = {
                  recipeId: this.state.recipeId,
                  cocktailName: this.state.cocktailName,
                  bartender: this.state.bartender,
                  location: this.state.bartender,
                  glasswareName: this.state.glasswareName
                }

    this.props.onFormSubmit(submit_data);
    this.setState(this.initialState);
  }

  render() {

    let pageTitle;
    if(!this.state.isAdd) {
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
              <Form.Row>
                <Form.Group as={Col} controlId="cocktailName">
                  <Form.Label>Cocktail Name</Form.Label>
                  <Form.Control
                    required
                    type="text"
                    name="cocktailName"
                    value={this.state.cocktailName}
                    onChange={this.handleChange}
                    placeholder=""/>
                </Form.Group>
                <Form.Group as={Col} controlId="bartender">
                  <Form.Label>Bartender</Form.Label>
                  <Form.Control
                    type="text"
                    name="bartender"
                    value={this.state.bartender}
                    onChange={this.handleChange}
                    placeholder=""/>
                </Form.Group>
              </Form.Row>
              <Form.Row>
                <Form.Group as={Col}  controlId="location">
                  <Form.Label>Location</Form.Label>
                  <Form.Control
                    type="text"
                    name="location"
                    value={this.state.location}
                    onChange={this.handleChange}
                    placeholder=""/>
                </Form.Group>
                <Form.Group as={Col}  controlId="glasswareName">
                  <Form.Label>Glassware Name</Form.Label>
                  <Form.Control
                    type="text"
                    name="glasswareName"
                    value={this.state.glasswareName}
                    onChange={this.handleChange}
                    placeholder=""/>
                </Form.Group>
              </Form.Row>
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
