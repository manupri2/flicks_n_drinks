import React, {Component} from 'react';
import { Container, Button, Nav, NavLink, Navbar,  Alert, Form, ButtonGroup, Row } from 'react-bootstrap';
import { PlusCircle } from 'react-bootstrap-icons';
import MovieList from './MovieList';
import MovieQueryForm from './MovieQueryForm';
import CocktailList from './CocktailList';
import CocktailQueryForm from './CocktailQueryForm';
import AddMovie from './AddMovie';
import AddCocktail from './AddCocktail';

import UserApp from './userApp';
import ReactDOM from 'react-dom';


// just some scrap code i want to keep around as i think it may be useful
// can put put it inside "componentDidMount()" for a component class and it will run this.test_Query() every 5000 ms
// this will be useful for any auto update functions (i.e. showing a ticking clock):
//
// this.timerID = setInterval(() => this.test_Query(), 5000);

class CRUDApp extends Component {
  constructor(props) {
    super(props);

        this.state = {
          user: this.props.usertoCURD,
          isAddItem: false,
          error: null,
          isLoaded: true,
          response: {},
          database: this.props.usertoCURD.database? "Cocktails":"Movies",
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
    this.setState({ isAddItem: true,
                    isEditItem: false });
  }

  updateFilters(new_filters) {
    this.setState(state => ({
                        filters: new_filters,
                        error: null,
                        isLoaded: false
                        }));
  }

  onFormSubmit(data) {
    
//    if(data.isAdd){
//      delete data["isAdd"];
   //   data.genre = parseInt(data.genre);
   // }
    
    var db = this.state.database.slice(0, -1);
    var apiUrl = 'http://cs411ccsquad.web.illinois.edu/';
    var data_json_uri = encodeURI(JSON.stringify(data));
    console.log(JSON.stringify(data))
    
    if(this.state.isEditItem){
      apiUrl += "edit/" + db + "/" + data_json_uri;
    } else {
      apiUrl += "add/" + db + "/" + data_json_uri;
    }

    
 //   if(this.state.isEditItem && this.state.database == "Movies"){
      ////apiUrl += "edit/" + db + "/" + data.tconst.toString() + "/" + data.title;
 //     apiUrl += "edit/" + db + "/" + data_json_uri;
  //  } else if (!this.state.isEditItem && this.state.database == "Movies") {
  //    apiUrl += "add/" + db + "/" + data_json_uri;

  //  } else if (this.state.isEditItem && this.state.database == "Cocktails") {
     //// apiUrl += "edit/" + db + "/" + data.recipeId.toString() + "/" + data.cocktailName;
  //   apiUrl += "edit/" + db + "/" + data_json_uri;
 //   } else if (!this.state.isEditItem && this.state.database == "Cocktails") {
  //    apiUrl += "add/" + db + "/" + data_json_uri;
  //  }
 
    fetch(apiUrl);
    this.setState({
          isAddItem: false,
          isEditItem: false,
          isLoaded: false,
          curr_item: {}
        })
  }

  editItem = item_id => {

        var filter_info = Object.assign({}, this.state.filters);

        if(this.state.database == "Movies"){
            filter_info['tConst'] = {value: item_id, operator: '=', label: ""};
        } else {
            filter_info['recipeId'] = {value: item_id, operator: '=', label: ""};
        }

        var api_url = 'http://cs411ccsquad.web.illinois.edu/read/';
        var db = this.state.database
        var filters = encodeURI(JSON.stringify(filter_info));
        api_url += db + "/" + filters;

        fetch(api_url)
          .then(res => res.json())
          .then(
            (result) => {
              this.setState({
                curr_item: result.data[0],
                isEditItem: true,
                isAddItem: false
              });
            },
            (error) => {
              this.setState({error});
            }
          )
  }


  changeDB(new_db) {
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


  rateMovie = (item_id, rating) => {
    var api_url = 'http://cs411ccsquad.web.illinois.edu/vote/';
    var db = this.state.database.slice(0, -1)

    var filter_info = {userId: this.state.user.userId, tConst: item_id, ratesMovie: rating};
    var filters = encodeURI(JSON.stringify(filter_info));

    api_url += db + "/" + filters;
    console.log(JSON.stringify(filter_info));
    fetch(api_url);
    this.setState({
                    isLoaded: false,
                    error: null
                });
  }


  searchItems() {
            var api_url = 'http://cs411ccsquad.web.illinois.edu/read/';
            var db = this.state.database;
            var filters = Object.assign({}, this.state.filters);
            filters["userId"] = this.state.user.userId;

            var filters_str = encodeURI(JSON.stringify(filters));
            api_url += db + "/" + filters_str;

            console.log(api_url)
            console.log(JSON.stringify(filters))

            if(!this.state.isLoaded){
                fetch(api_url)
                    .then(res => res.json())
                    .then(
                        (result) => {
                            console.log("Yayy!!!");
                            console.log(result.data);
                            this.setState({
                                isLoaded: true,
                                items: result.data,
                                error: null
                            });
                        },
                        (error) => {
                            console.log("Nooooo!!!");
                            this.setState({
                                isLoaded: true,
                                error
                            });
                        }
                    )
            }
  }



  deleteItem(item_id) {
    const apiUrl = 'http://cs411ccsquad.web.illinois.edu/delete/' + this.state.database.slice(0, -1) + '/' + item_id.toString();
    fetch(apiUrl);
    this.setState(state => ({
                          error: null,
                          isLoaded: false,
                          items: [],
                    }));
  }


  navtoUserPage(){
    console.log(this.state.user)
    ReactDOM.unmountComponentAtNode(document.getElementById('root'));     
    ReactDOM.render(<UserApp userDetails ={this.state.user}/>, document.getElementById('root'));
  }


  render() {
    let itemForm;
    if(this.state.isAddItem || this.state.isEditItem) {
      var item = Object.assign({}, this.onFormSubmit);
      item["isAdd"] = 1;
        if(this.state.database == "Movies") {
            itemForm = <AddMovie onFormSubmit={this.onFormSubmit} item={this.state.curr_item}  isAdd={this.state.isAddItem}/>
        } else {
            itemForm = <AddCocktail onFormSubmit={this.onFormSubmit} item={this.state.curr_item} isAdd={this.state.isAddItem}/>
        }
    }

    this.searchItems();

    return (
      <div>
            <Navbar bg="dark" variant="dark">   
                <Navbar.Brand href="">Flicks n Drinks</Navbar.Brand>
                    <Nav className="mr-auto">
                        <Button variant="dark"  onClick={() => this.navtoUserPage()} > My profile </Button>
                        <Button variant="dark"  onClick={() => this.changeDB("Movies")}> Movies </Button>
                        <Button variant="dark"  onClick={() => this.changeDB("Cocktails")}> Cocktails </Button>
                    </Nav>  
                    <Nav className="justify-content-end" activeKey="">
                        <Nav.Item>
                            <Nav.Link href="/flicks_n_drinks">Logout</Nav.Link>
                        </Nav.Item>
                    </Nav>
            </Navbar>

        <Container>
          <Row><br/><br/><br/></Row>

          <Row>

          </Row>


          <Row>
              {this.state.response.status === 'success' && <div><br /><Alert variant="info">{this.state.response.message}</Alert></div>}
              {!this.state.isAddItem && !this.state.isEditItem && <div class="text-right pr-0"><Button variant="primary" onClick={() => this.onCreate()}>Add {this.state.database.slice(0, -1)} <PlusCircle /></Button><br /><br /></div>}
          </Row>
          
          {!this.state.isAddItem && !this.state.isEditItem && this.state.database == "Movies" && <MovieQueryForm updateFilters={this.updateFilters}/>}
          {!this.state.isAddItem && !this.state.isEditItem && this.state.database == "Movies" && <MovieList editItem={this.editItem} deleteItem={this.deleteItem} rateMovie={this.rateMovie} info={this.state}/>}
          {!this.state.isAddItem && !this.state.isEditItem && this.state.database == "Cocktails" && <CocktailQueryForm updateFilters={this.updateFilters}/>}
          {!this.state.isAddItem && !this.state.isEditItem && this.state.database == "Cocktails" && <CocktailList editItem={this.editItem} deleteItem={this.deleteItem} info={this.state}/>}

          {itemForm}
          {this.state.error && <div>Error: {this.state.error.message}</div>}
        </Container>
      </div>
    );
  }
}

export default CRUDApp;
