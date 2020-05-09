import React from 'react';
import { Table, Button, Alert, Spinner } from 'react-bootstrap';

class TopGenres extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        top_genres: []
    }
  }


  render() {
      const genres = this.props.genres;

      return(
        <div>
        <h2>Your Top Genres</h2>
        <ol>
              {genres.map(genre => (
                <li>{genre}</li>
              ))}
        </ol>
        </div>
      )
    }
  }

export default TopGenres;
