import React, {Component} from 'react';
import { Container, Button, Alert, Form } from 'react-bootstrap';
import MovieList from './MovieList';
import MovieQueryForm from './MovieQueryForm';
import AddMovie from './AddMovie';


class CRUDApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAddMovie: false,
      error: null,
      isLoaded: true,
      response: {},
      items: [],
      movie: {},
      filters: {title: "", year: "2017", rating: ""},
      isEditMovie: false,
      query: ""
    }
    this.onFormSubmit = this.onFormSubmit.bind(this);
    this.updateFilters = this.updateFilters.bind(this);
    this.searchMovie = this.searchMovie.bind(this);
  }

  onCreate() {
    this.setState({ isAddMovie: true });
  }

  updateFilters(new_filters) {
    this.setState(state => ({
                        filters: new_filters,
                        error: null,
                        isLoaded: false
                        }));
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
          this.setState({error});
        }
      )
  }

  searchMovie() {
            var api_url = 'http://cs411ccsquad.web.illinois.edu/Movie/';
            var filters = encodeURI(JSON.stringify(this.state.filters));
            api_url += filters;

            if(!this.state.isLoaded){
                fetch(api_url)
                    .then(res => res.json())
                    .then(
                        (result) => {
                            this.setState({
                                isLoaded: true,
                                items: result.data,
                                error: null,
                                query: api_url
                            });
                        },
                        (error) => {
                            this.setState({
                                isLoaded: true,
                                query: api_url,
                                error
                            });
                        }
                    )
            }
  }

  render() {
    let movieForm;
    if(this.state.isAddMovie || this.state.isEditMovie) {
      movieForm = <AddMovie onFormSubmit={this.onFormSubmit} movie={this.state.movie} />
    }

    this.searchMovie();

    return (
      <div>
        {!this.state.isAddMovie && <Button variant="primary" onClick={() => this.onCreate()}>Add Movie</Button>}
        <Container>
          <MovieQueryForm updateFilters={this.updateFilters}/>
          {this.state.response.status === 'success' && <div><br /><Alert variant="info">{this.state.response.message}</Alert></div>}
          {!this.state.isAddMovie && <MovieList editMovie={this.editMovie} info={this.state}/>}
          {movieForm}
          {this.state.error && <div>Error: {this.state.error.message}</div>}
        </Container>
      </div>
    );
  }
}

export default CRUDApp;