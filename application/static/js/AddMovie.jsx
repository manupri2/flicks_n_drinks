import React from 'react';
import { Row, Form, Col, Button } from 'react-bootstrap';

class AddMovie extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
      tConst: '',
      title: '',
      year: 0,
      genre: 1,
      isAdd: props.isAdd
    }

    if(props.isAdd){
      this.state = this.initialState;
    } else {
      this.state = {
                      tConst: props.item.tConst,
                      title: props.item.title,
                      year: props.item.year,
                      genre: 1,
                      isAdd: false
                    }
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const name = event.target.name;
    var value = event.target.value;
    let new_value;
    
    if(name == "year"){
        if(value == ""){
            new_value = 0;
        } else {
            new_value = parseInt(value, 10);
        }

    } else if (name == "title"){
        new_value = value;
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

    var submit_data = {
                      tConst: this.state.tConst,
                      title: this.state.title,
                      year: this.state.year,
                      genre: parseInt(this.state.genre, 10)
                    }

    this.props.onFormSubmit(submit_data);
    this.setState(this.initialState);
  }


  showGenre(){
  if (this.state.isAdd) {
      return(
      <Form.Group as={Col} controlId="genre">
      <Form.Label>Genre</Form.Label>
      <Form.Control 
        as = "select"
        name = "genre"
        value = {this.state.genre}
        onChange={this.handleChange}>
        <option value = {0}>Romance</option>
        <option value = {1}>Biography</option>
        <option value = {2}>Crime</option>
        <option value = {3}>Drama</option>
        <option value = {4}>Adventure</option>
        <option value = {5}>Family</option>
        <option value = {6}>History</option>
        <option value = {7}>Fantasy</option>
        <option value = {8}>War</option>
        <option value = {9}>Thriller</option>
        <option value = {10}>Documentary</option>
        <option value = {11}>Comedy</option>
        <option value = {12}>Mystery</option>
        <option value = {13}>Horror</option>
        <option value = {14}>Western</option>
        <option value = {15}>Music</option>
        <option value = {16}>Action</option>
        <option value = {17}>Sci-Fi</option>
        <option value = {18}>Animation</option>
        <option value = {19}>Musical</option>
        <option value = {20}>Sport</option>
        <option value = {21}>Film-Noir</option>
        <option value = {22}>News</option>
        <option value = {23}>Talk-Show</option>
        <option value = {24}>Adult</option>
      </Form.Control>
    </Form.Group>)
    }

  }

  render() {

    let pageTitle;
    if(!this.state.isAdd) {
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

              
              {this.showGenre()}


              </Form.Row>
              <Form.Group>
                <Form.Control type="hidden" name="tConst" value={this.state.tConst} />
                <Button variant="success" type="submit" >Save</Button>
                
              </Form.Group>
            </Form>
          </Col>
        </Row>

      </div>
    )
  }
}

export default AddMovie;
