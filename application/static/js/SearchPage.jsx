import React, { Component } from 'react';
require('../css/fullstack.css');
import { Container, Button, Alert } from 'react-bootstrap';
import MovieList from './MovieList';


class SearchPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAddMovie: false,
      error: null,
      response: {},
      movie: {},
      isEditMovie: false
    }
    this.onFormSubmit = this.onFormSubmit.bind(this);
  }

  onCreate() {
    this.setState({ isAddMovie: true });
  }

  onFormSubmit(data) {
    let apiUrl;

    if(this.state.isEditMovie){
      apiUrl = 'http://localhost/dev/tcxapp/reactapi/editProduct';
    } else {
      apiUrl = 'http://localhost/dev/tcxapp/reactapi/createProduct';
    }

    const myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      myHeaders
    };

    fetch(apiUrl, options)
      .then(res => res.json())
      .then(result => {
        this.setState({
          response: result,
          isAddMovie: false,
          isEditMovie: false
        })
      },
      (error) => {
        this.setState({ error });
      }
    )
  }

  editMovie = tconst => {

    const apiUrl = 'http://localhost/dev/tcxapp/reactapi/getProduct';
    const formData = new FormData();
    formData.append('tconst', tconst);

    const options = {
      method: 'POST',
      body: formData
    }

    fetch(apiUrl, options)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            movie: result.data,
            isEditMovie: true,
            isAddMovie: true
          });
        },
        (error) => {
          this.setState({ error });
        }
      )
  }

  render() {

    let movieForm;
    if(this.state.isAddMovie || this.state.isEditMovie) {
      movieForm = <AddMovie onFormSubmit={this.onFormSubmit} movie={this.state.movie} />
    }

    return (
      <div className="App">
        <Container>
          <h1 style={{textAlign:'center'}}>React Tutorial</h1>
          {!this.state.isAddMovie && <Button variant="primary" onClick={() => this.onCreate()}>Add Movie</Button>}
          {this.state.response.status === 'success' && <div><br /><Alert variant="info">{this.state.response.message}</Alert></div>}
          {!this.state.isAddMovie && <MovieList editMovie={this.editMovie}/>}
          {movieForm}
          {this.state.error && <div>Error: {this.state.error.message}</div>}
        </Container>
      </div>
    );
  }
}

export default SearchPage;