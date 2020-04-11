import React from 'react';
import { Table, Button, Alert } from 'react-bootstrap';

class MovieList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      movies: [],
      isLoaded: false,
      response: {},
      api_url: 'http://cs411ccsquad.web.illinois.edu/Movie/',
      filters: {title: "", year: "2015", rating: ""}
    }
  }

  componentDidMount() {
    var apiUrl = this.state.api_url;
    var filters = encodeURI(JSON.stringify(this.state.filters));
    apiUrl += filters;

    fetch(apiUrl)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
                movies: result.data,
                isLoaded: true,
                error: null
          });
        },
        (error) => {
          this.setState({isLoaded: true, error });
        }
      )
  }

  deleteProduct(tconst) {
    const {movies} = this.state;

    const apiUrl = 'http://localhost/dev/tcxapp/reactapi/deleteProduct';
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
            response: result,
            movies: movies.filter(movie => movie.tconst !== tconst)
          });
        },
        (error) => {
          this.setState({ error });
        }
      )
  }

  render() {
    const {error, movies, isLoaded} = this.state;

    if(error) {
      return (
        <div>Error: {error.message}</div>
      )
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
                    &nbsp;<Button variant="danger">Delete</Button>
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
