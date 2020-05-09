import React from 'react';
import { Table, Button, Alert, Spinner } from 'react-bootstrap';

class MovieList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        response: {}
    }
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
                <tr key={movie.tConst}>
                  <td>{movie.title}</td>
                  <td>{movie.year}</td>
                  <td>{movie.rating}</td>
                  <td>{movie.crew}</td>
                  <td>{movie.genres}</td>
                  <td>
                    <Button variant="info" onClick={() => this.props.editItem(movie.tConst)}>Edit</Button>
                    &nbsp;<Button variant="danger" onClick={() => this.props.deleteItem(movie.tConst)}>Delete</Button>
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
