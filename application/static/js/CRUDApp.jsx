import React, {Component} from 'react';
import { Container, Button, Alert, Form, ButtonGroup } from 'react-bootstrap';
import { PlusCircle } from 'react-bootstrap-icons';
import MovieList from './MovieList';
import MovieQueryForm from './MovieQueryForm';
import CocktailList from './CocktailList';
import CocktailQueryForm from './CocktailQueryForm';
import AddMovie from './AddMovie';
import AddCocktail from './AddCocktail';

// just some scrap code i want to keep around as i think it may be useful
// can put put it inside "componentDidMount()" for a component class and it will run this.test_Query() every 5000 ms
// this will be useful for any auto update functions (i.e. showing a ticking clock):
//
// this.timerID = setInterval(() => this.test_Query(), 5000);

class CRUDApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
          isAddItem: false,
          error: null,
          isLoaded: true,
          response: {},
          database: "Movies",
          items: [],
          deleted_item: {},
          curr_item: {},
          filters: {},
          isEditItem: false
        }

    this.onFormSubmit = this.onFormSubmit.bind(this);
    this.updateFilters = this.updateFilters.bind(this);
    this.searchItems = this.searchItems.bind(this);
    this.changeDB = this.changeDB.bind(this);
    this.deleteItem = this.deleteItem.bind(this);
  }

  onCreate() {
    this.setState({ isAddItem: true });
  }

  updateFilters(new_filters) {
    this.setState(state => ({
                        filters: new_filters,
                        error: null,
                        isLoaded: false
                        }));
  }

  onFormSubmit(data) {
    var db = this.state.database.slice(0, -1);
    var apiUrl = 'http://cs411ccsquad.web.illinois.edu/';


    if(this.state.isEditItem && this.state.database == "Movies"){
      apiUrl += "edit/" + db + "/" + data.tconst.toString() + "/" + data.title;
    } else if (!this.state.isEditItem && this.state.database == "Movies") {
      apiUrl += "add/" + db + "/" + data.title;

    } else if (this.state.isEditItem && this.state.database == "Cocktails") {
      apiUrl += "edit/" + db + "/" + data.recipeId.toString() + "/" + data.cocktailName;
    } else if (!this.state.isEditItem && this.state.database == "Cocktails") {
      apiUrl += "add/" + db + "/" + data.cocktailName;
    }


    //const myHeaders = new Headers();
    //myHeaders.append('Content-Type', 'application/json');

    //const options = {
     // method: 'POST',
     // body: JSON.stringify(data),
     // myHeaders
    //

    fetch(apiUrl);
    this.setState({
          isAddItem: false,
          isEditItem: false,
          isLoaded: false
        })
  }

  editItem = item_id => {

        //const apiUrl = 'http://localhost/dev/tcxapp/reactapi/getProduct';
        //const formData = new FormData();
        //formData.append('tconst', tconst);
        var filter_info = Object.assign({}, this.state.filters);

        if(this.state.database == "Movies"){
            filter_info['Movie.tconst'] = {value: item_id.toString(), operator: '=', label: ""};
        } else {
            filter_info['CocktailRecipe.recipeId'] = {value: item_id.toString(), operator: '=', label: ""};
        }

        var api_url = 'http://cs411ccsquad.web.illinois.edu/';
        var db = this.state.database
        var filters = encodeURI(JSON.stringify(filter_info));
        api_url += db + "/" + filters;

        //const options = {
        //  method: 'POST',
         // body: formData
        //

        fetch(api_url)
          .then(res => res.json())
          .then(
            (result) => {
              this.setState({
                curr_item: result.data[0],
                isEditItem: true,
                isAddItem: true
              });
            },
            (error) => {
              this.setState({error});
            }
          )
      }


  changeDB(new_db) {

        console.log(new_db);

        this.setState(state => ({
                                  isAddItem: false,
                                  error: null,
                                  isLoaded: true,
                                  response: {},
                                  database: new_db,
                                  items: [],
                                  curr_item: {},
                                  filters: {},
                                  isEditItem: false
                            }));
  }


  searchItems() {
            var api_url = 'http://cs411ccsquad.web.illinois.edu/read/';
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



  deleteItem(item_id) {
    // const {movies} = this.state;

    const apiUrl = 'http://cs411ccsquad.web.illinois.edu/delete/' + this.state.database.slice(0, -1) + '/' + item_id.toString();
    // console.log(apiUrl)

    // const formData = new FormData();
    // formData.append('tconst', tconst);

    // const options = {
    //   method: 'GET',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({product_id:tconst})
    // }

    fetch(apiUrl);

    this.setState(state => ({
                          error: null,
                          isLoaded: false,
                          items: [],
                    }));
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
    let itemForm;
    if(this.state.isAddItem || this.state.isEditItem) {
        if(this.state.database == "Movies") {
            itemForm = <AddMovie onFormSubmit={this.onFormSubmit} item={this.state.curr_item} />
        } else {
            itemForm = <AddCocktail onFormSubmit={this.onFormSubmit} item={this.state.curr_item} />
        }
    }

    this.searchItems();

    return (
      <div>
        <ButtonGroup aria-label="Select database">
          <Button variant="secondary" onClick={() => this.changeDB("Movies")}>Movies</Button>
          <Button variant="secondary" onClick={() => this.changeDB("Cocktails")}>Cocktails</Button>
        </ButtonGroup>

        <Container>
          {this.state.response.status === 'success' && <div><br /><Alert variant="info">{this.state.response.message}</Alert></div>}
          {!this.state.isAddItem && <div class="text-right pr-0"><Button variant="primary" onClick={() => this.onCreate()}>Add {this.state.database.slice(0, -1)} <PlusCircle /></Button><br /><br /></div>}

          {!this.state.isAddItem && this.state.database == "Movies" && <MovieQueryForm updateFilters={this.updateFilters}/>}
          {!this.state.isAddItem && this.state.database == "Movies" && <MovieList editItem={this.editItem} deleteItem={this.deleteItem} info={this.state}/>}
          {!this.state.isAddItem && this.state.database == "Cocktails" && <CocktailQueryForm updateFilters={this.updateFilters}/>}
          {!this.state.isAddItem && this.state.database == "Cocktails" && <CocktailList editItem={this.editItem} deleteItem={this.deleteItem} info={this.state}/>}

          {itemForm}
          {this.state.error && <div>Error: {this.state.error.message}</div>}
        </Container>
      </div>
    );
  }
}

export default CRUDApp;