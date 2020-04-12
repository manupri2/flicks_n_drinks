import React, {Component} from 'react';
import { Container, Button, Alert, Form, ButtonGroup } from 'react-bootstrap';
import { PlusCircle } from 'react-bootstrap-icons';
import MovieList from './MovieList';
import MovieQueryForm from './MovieQueryForm';
import CocktailList from './CocktailList';
import CocktailQueryForm from './CocktailQueryForm';
import AddMovie from './AddMovie';


class CRUDApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
          isAddMovie: false,
          error: null,
          isLoaded: true,
          response: {},
          database: "Movies",
          items: [],
          deleted_item: {},
          movie: {},
          filters: {},
          isEditMovie: false
        }

    this.onFormSubmit = this.onFormSubmit.bind(this);
    this.updateFilters = this.updateFilters.bind(this);
    this.searchMovie = this.searchMovie.bind(this);
    this.changeDB = this.changeDB.bind(this);
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


  changeDB(new_db){

        console.log(new_db);

        this.setState(state => ({
                                  isAddMovie: false,
                                  error: null,
                                  isLoaded: true,
                                  response: {},
                                  database: new_db,
                                  items: [],
                                  movie: {},
                                  filters: {},
                                  isEditMovie: false
                            }));
  }


  searchMovie() {
            var api_url = 'http://cs411ccsquad.web.illinois.edu/';
            var db = this.state.database
            var filters = encodeURI(JSON.stringify(this.state.filters));
            api_url += db + "/" + filters;

            if(!this.state.isLoaded){
                fetch(api_url)
                    .then(res => res.json())
                    .then(
                        (result) => {
                            this.setState({
                                isLoaded: true,
                                items: result.data,
                                error: null
                            });
                        },
                        (error) => {
                            this.setState({
                                isLoaded: true,
                                error
                            });
                        }
                    )
            }
  }



  deleteMovie(tconst) {
    // const {movies} = this.state;

    const apiUrl = 'http://cs411ccsquad.web.illinois.edu/delete/Movie/'+ tconst.toString();
    // console.log(apiUrl)

    // const formData = new FormData();
    // formData.append('tconst', tconst);

    // const options = {
    //   method: 'GET',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({product_id:tconst})
    // }

    fetch(apiUrl)
      .then(res => res.json())
      .then(
          (result) => {
              this.setState({
                  isLoaded: false,
                  deleted_item: result.data,
                  error: null
              });
          },
          (error) => {
              this.setState({
                  isLoaded: true,
                  error
              });
          }
      )

    // const arrayCopy = this.props.info.items.filter((row) => row.tconst != tconst);
    // this.setState({movies:arrayCopy});



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
    let movieForm;
    if(this.state.isAddMovie || this.state.isEditMovie) {
      movieForm = <AddMovie onFormSubmit={this.onFormSubmit} movie={this.state.movie} />
    }

    this.searchMovie();

    return (
      <div>
        <ButtonGroup aria-label="Select database">
          <Button variant="secondary" onClick={() => this.changeDB("Movies")}>Movies</Button>
          <Button variant="secondary" onClick={() => this.changeDB("Cocktails")}>Cocktails</Button>
        </ButtonGroup>

        <Container>
          {this.state.response.status === 'success' && <div><br /><Alert variant="info">{this.state.response.message}</Alert></div>}
          {!this.state.isAddMovie && <div class="text-right pr-0"><Button variant="primary" onClick={() => this.onCreate()}>Add {this.state.database.slice(0, -1)} <PlusCircle /></Button><br /><br /></div>}
          {!this.state.isAddMovie && this.state.database == "Movies" && <MovieQueryForm updateFilters={this.updateFilters}/>}
          {!this.state.isAddMovie && this.state.database == "Movies" && <MovieList editMovie={this.editMovie} deleteMovie={this.deleteMovie} info={this.state}/>}
          {!this.state.isAddMovie && this.state.database == "Cocktails" && <CocktailQueryForm updateFilters={this.updateFilters}/>}
          {!this.state.isAddMovie && this.state.database == "Cocktails" && <CocktailList editItem={this.editMovie} info={this.state}/>}

          {movieForm}
          {this.state.error && <div>Error: {this.state.error.message}</div>}
        </Container>
      </div>
    );
  }
}

export default CRUDApp;