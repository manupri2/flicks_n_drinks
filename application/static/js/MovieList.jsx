import React, { useState } from 'react';
import { Table, Button, ToggleButton, ToggleButtonGroup, Alert, Spinner } from 'react-bootstrap';

class MovieList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        response: {},
    } 
    // const [value, setValue] = useState([1,3])
  //  this.handleChange = this.handleChange.bind(this);
  }

 //  handleChange (event) {
 //   this.setState({
//       const: [value, setValue] = useState([1,3])
 //    });
 //  }

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
                <th>Personal Rating</th>
                <th>Crew</th>
                <th>Genres</th>
                <th>Vote</th>
                <th>Edit/Delete</th>
              </tr>
            </thead>
            <tbody>
              {movies.map(movie => (
                <tr key={movie.tConst}>
                  <td>{movie.title}</td>
                  <td>{movie.year}</td>
                  <td>{movie.rating}</td>
                  <td>{movie.personalRating}</td>
                  <td>{movie.crew}</td>
                  <td>{movie.genres}</td>
                  <td>
                  <ToggleButtonGroup type="radio" value={movie.ratesMovie} name="options">
                    <ToggleButton value={1} onClick={() => this.props.rateMovie(movie.tConst, 1)}>1</ToggleButton>
                    <ToggleButton value={2} onClick={() => this.props.rateMovie(movie.tConst, 2)}>2</ToggleButton>
                    <ToggleButton value={3} onClick={() => this.props.rateMovie(movie.tConst, 3)}>3</ToggleButton>
                    <ToggleButton value={4} onClick={() => this.props.rateMovie(movie.tConst, 4)}>4</ToggleButton>
                    <ToggleButton value={5} onClick={() => this.props.rateMovie(movie.tConst, 5)}>5</ToggleButton>
                    <ToggleButton value={6} onClick={() => this.props.rateMovie(movie.tConst, 6)}>6</ToggleButton>
                    <ToggleButton value={7} onClick={() => this.props.rateMovie(movie.tConst, 7)}>7</ToggleButton>
                    <ToggleButton value={8} onClick={() => this.props.rateMovie(movie.tConst, 8)}>8</ToggleButton>
                    <ToggleButton value={9} onClick={() => this.props.rateMovie(movie.tConst, 9)}>9</ToggleButton>
                    <ToggleButton value={10} onClick={() => this.props.rateMovie(movie.tConst, 10)}>10</ToggleButton>
                  </ToggleButtonGroup>
                  </td>
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
