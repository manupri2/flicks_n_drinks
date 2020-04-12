import React from 'react';
import { Table, Button, Alert, Spinner } from 'react-bootstrap';

class MovieList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      response: {}
    }
  }

  deleteProduct(tconst) {
    const {movies} = this.state;


    const arrayCopy = this.state.products.filter((row) => row.tconst != tconst);
    this.setState({products:arrayCopy});


    // const apiUrl = 'http://localhost:5000/delete';
    const apiUrl = 'http://cs411ccsquad.web.illinois.edu/CocktailName/delete';
    const formData = new FormData();
    formData.append('tconst', tconst);

    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({database:this.state.database, product_id:tconst})
    }

    fetch(apiUrl,options)
    // fetch(apiUrl, options)
    //   .then(res => res.json())
    //   .then(
    //     (result) => {
    //       this.setState({
    //         response: result,
    //         movies: movies.filter(movie => movie.tconst !== tconst)
    //       });
    //     },
    //     (error) => {
    //       this.setState({ error });
    //     }
    //   )
  }

  render() {
    const error = this.props.info.error;
    const movies = this.props.info.items;
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
          <h2>Movie List</h2>
          {this.state.response.message && <Alert variant="info">{this.state.response.message}</Alert>}
          <Table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Year</th>
                <th>Rating</th>
                <th>Crew</th>
                <th>Genres</th>
                <th>Edit/Delete</th>
              </tr>
            </thead>
            <tbody>
              {movies.map(movie => (
                <tr key={movie.tconst}>
                  <td>{movie.title}</td>
                  <td>{movie.year}</td>
                  <td>{movie.rating}</td>
                  <td>{movie.crew}</td>
                  <td>{movie.genres}</td>
                  <td>
                    <Button variant="info" onClick={() => this.props.editMovie(movie.tconst)}>Edit</Button>
                    &nbsp;<Button variant="danger" onClick={() => this.deleteMovie(mocie.tconst)}>Delete</Button>
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

export default MovieList;
