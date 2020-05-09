import React from 'react';
import { Row, Form, Col, Button } from 'react-bootstrap';

class AddMovie extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
      tConst: '',
      title: 'Test',
      year: 0,
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
    var value = event.target.value;
    let new_value;

    if(name == "year"){
        new_value = parseInt(value, 10);
    } else {
        new_value = value;
    }

    var value = event.target.value;
    this.setState({
      [name]: new_value
    })

  }

  handleSubmit(event) {
    event.preventDefault();
    //var state_copy = this.state;
    //delete state_copy['tConst'];
    //this.props.onFormSubmit(state_copy);
    //this.setState(this.initialState);

    this.props.onFormSubmit(this.state);
    this.setState(this.initialState);
  }

  render() {

    let pageTitle;
    if(this.state.tConst>=0) {
      pageTitle = <h2>Edit Movie</h2>
    } else {
      pageTitle = <h2>Add Movie</h2>
    }

    return(
      <div>
        {pageTitle}
        <Row>
          <Col sm={6}>
            <Form onSubmit={this.handleSubmit}>
              <Form.Row>
              <Form.Group as={Col} controlId="title">
                <Form.Label>Movie Title</Form.Label>
                <Form.Control
                  required
                  type="text"
                  name="title"
                  value={this.state.title}
                  onChange={this.handleChange}
                  placeholder=""/>
              </Form.Group>
              <Form.Group as={Col} controlId="year">
                <Form.Label>Year</Form.Label>
                <Form.Control
                  type="text"
                  name="year"
                  value={this.state.year}
                  onChange={this.handleChange}
                  placeholder=""/>
              </Form.Group>
              </Form.Row>
              <Form.Group>
                <Form.Control type="hidden" name="tConst" value={this.state.tConst} />
                <Button variant="success" type="submit">Save</Button>
              </Form.Group>
            </Form>
          </Col>
        </Row>
      </div>
    )
  }
}

export default AddMovie;
