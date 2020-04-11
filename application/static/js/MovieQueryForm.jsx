import React from 'react';
import { Row, Form, Col, Button } from 'react-bootstrap';


class MovieQueryForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          title: '',
          year: '',
          rating: ''
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
    const value = event.target.value;

    this.setState({
      [name]: value
    });
  }

    render() {

          return(
              <Form onSubmit={this.handleSubmit}>

                  <Row>
                      <Col>
                          <Form.Row>
                                <Form.Group controlId="Title">
                                  <Form.Label>Title:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="title"
                                        value={this.state.title}
                                        onChange={this.handleChange}
                                        placeholder="Enter title" />
                                </Form.Group>

                                <Form.Group controlId="Year">
                                  <Form.Label>Year:</Form.Label>
                                  <Form.Control
                                        type="text"
                                        name="year"
                                        value={this.state.year}
                                        onChange={this.handleChange}
                                        placeholder="YYYY" />
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

export default MovieQueryForm;