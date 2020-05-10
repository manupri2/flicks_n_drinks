import React, {Component} from 'react';
import Chart from "react-apexcharts";
import {Table, Container, Row, Col, Button, Nav, Navbar, OverlayTrigger, Popover} from 'react-bootstrap';
import Modal from 'react-awesome-modal';
import ReactDOM from 'react-dom';
import CRUDApp from './CRUDApp';
import TopGenres from './TopGenres';

import AutoUserList from './AutoUserList'

class UserApp extends Component {
    constructor(props) {
        super(props);

        let defaultUser = this.props.userDetails
        defaultUser["isMaster"]=1

        this.state = {

            user: [defaultUser,
            ],
            genresLoaded: false,
            topGenres: [],
            chart: {
                options: {
                    title: {
                        text: 'Personality',
                        align: 'middle',
                        style: {
                            fontSize: '24px'
                        }
                    },
                    xaxis: {
                        categories: ['Openness', 'Conscientiousness', 'Extroversion', 'Agreeableness', 'Neuroticism'],
                        labels: {
                            style: {
                                fontSize: '14px'
                            }
                        }
                    },
                    yaxis: {
                        min: 0,
                        max: 100,
                        tickAmount: 5,

                    }
                },

            },

            addFriendPopup: false,
            deleteFriendPopup: false,
            editPersonalityPopup: false,
            editPersonalityResult: '',
            addSearch: {firstName: '', lastName: '', email: '', autoCompleteLoaded:'', displayUsers:[]},
            nextUserRank: 2
            
        }
        
        // this.showChart = this.showChart.bind(this)
        // this.handleChange_Openness = this.handleChange_Openness.bind(this)
        // this.handleChange_Conscientiousness = this.handleChange_Conscientiousness.bind(this)
        // this.handleChange_Extroversion = this.handleChange_Extroversion.bind(this)
        // this.handleChange_Agreeableness = this.handleChange_Agreeableness.bind(this)
        // this.handleChange_Neuroticism = this.handleChange_Neuroticism.bind(this)
        // this.getTopGenres = this.getTopGenres.bind(this)
        // this.submitPersonalityChange = this.submitPersonalityChange.bind(this)
        // this.addFriend= this.addFriend.bind(this)
        // this.deleteFriend= this.deleteFriend.bind(this)

        this.submitAddFriendAuto = this.submitAddFriendAuto.bind(this)


    }

    showChart() {

        const newSeries = []
        this.state.user.map((u) => {
            const tr_list = [u.trOpen, u.trCon, u.trEx, u.trAg, u.trNe];
            const data = tr_list.map((tr) => {
                return tr
            });
            newSeries.push({data, name: u.firstName + ' ' + u.lastName})
        })

        return (
            <Chart
                options={this.state.chart.options}
                series={newSeries}
                type="radar"
                width="800px"
                height="600px"

            />
        )
    }

    handleChange_Openness(e) {
        const input = e.target.value
        this.state.user[0]["trOpen"] = parseInt(input)
        this.forceUpdate()

    }

    handleChange_Conscientiousness(e) {
        const input = e.target.value
        this.state.user[0]["trCon"] = parseInt(input)
        this.forceUpdate()
    }

    handleChange_Extroversion(e) {
        const input = e.target.value
        this.state.user[0]["trEx"] = parseInt(input)
        this.forceUpdate()
    }

    handleChange_Agreeableness(e) {
        const input = e.target.value
        this.state.user[0]["trAg"] = parseInt(input)
        this.forceUpdate()
    }

    handleChange_Neuroticism(e) {
        const input = e.target.value
        this.state.user[0]["trNe"] = parseInt(input)
        this.forceUpdate()
    }

    submitPersonalityChange() {

        return (
            <div>
                <Button color='primary' onClick={() => this.openEditModal()}>Submit Change</Button>
                <Modal visible={this.state.editPersonalityPopup} width="800" height="400" effect="fadeInUp"
                       onClickAway={() => this.closeEditModal()}>
                    <h2>&nbsp;&nbsp;{this.state.editPersonalityResult.message}</h2>
                    <br/><br/><br/><br/><br/>
                    &nbsp;&nbsp;<Button color='primary' onClick={() => this.closeEditModal()}> Close </Button>
                </Modal>
            </div>
        )

    }

    openEditModal() {
        this.setState({
            editPersonalityPopup: true
        });

        var api_url = 'http://cs411ccsquad.web.illinois.edu/edit/User/';
        api_url += this.state.user[0].userId + '/'
        let open = this.state.user[0].trOpen;
        let con = this.state.user[0].trCon;
        let ext = this.state.user[0].trEx;
        let agr = this.state.user[0].trAg;
        let neu = this.state.user[0].trNe;
        const traits = [open, con, ext, agr, neu]
        for (const [index, value] of traits.entries()) {
            api_url += value + ":"
        }

        fetch(api_url)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({editPersonalityResult: result,
                                    genresLoaded: false
                                  })
                },
                (error) => {
                    this.setState({error})
                }
            )


    }

    closeEditModal() {
        this.setState({
            editPersonalityPopup: false
        });
    }


   getTopGenres() {
                  var api_url = 'http://cs411ccsquad.web.illinois.edu/MTNN/';
                  var filts = JSON.stringify({'userId': this.state.user[0].userId, 'tConst': []});
                  var filters = encodeURI(filts);

                  api_url += filters;

                if(!this.state.genresLoaded){
                fetch(api_url)
                    .then(res => res.json())
                    .then(
                                (result) => {
                                        var temp = "";
                                        var newGenres = [];

                                        for (var i = 0; i < result.length; i++) {
                                            temp = result[i].genreName;
                                            newGenres.push(temp);
                                        }

                                        this.setState({
                                            genresLoaded: true,
                                            topGenres: newGenres,
                                        });
                                },
                                (error) => {
                                            this.setState({
                                                genresLoaded: true,
                                                topGenres: []
                                            });
                                }
                    )
                }
    }


    addFriendPopup() {
        
        var users = this.state.addSearch.displayUsers
        // var submitAddFriend = this.props.submitAddFriend
        return (

            <div>
                <Button color="primary " onClick={() => this.openAddFriendModal()}> Add Friend </Button>
                <Modal visible={this.state.addFriendPopup} width="800" height="400" effect="fadeInUp"
                       onClickAway={() => this.closeAddFriendModal()}>
                    <div>
                        <h1>&nbsp;Adding Friend to Chart</h1>
                        &nbsp;<Button color="primary" onClick={() => this.searchAutoComplete()}> Search </Button>
                        &nbsp;<Button color="primary" onClick={() => this.closeAddFriendModal()}> Close </Button>
                        <Container>
                            <Row>&nbsp;</Row>
                            
                                
                            <Row>&nbsp;</Row>
                            <Row>
                                <Col sm={4}>
                                    <Row>&nbsp;<h4>First Name</h4></Row>
                                    <Row>
                                        &nbsp;<input type="text" name={'firstName'} placeholder="first name"
                                                     onChange={() => this.addFriendChange(event)}/>
                                    </Row>
                                </Col>

                                <Col sm={4}>
                                    <Row>&nbsp;<h4>Last Name</h4></Row>
                                    <Row>
                                        &nbsp;<input type="text" name={'lastName'} placeholder="last name"
                                                     onChange={() => this.addFriendChange(event)}/>
                                    </Row>
                                </Col>

                                <Col sm={4}>
                                    <Row>&nbsp;<h4>Email</h4></Row>
                                    <Row>
                                        &nbsp;<input type="text" name={'emailId'} placeholder="email"
                                                     onChange={() => this.addFriendChange(event)}/>
                                    </Row>
                                </Col>
                            </Row>
                            <div>
            <Table>
              <thead>
                <tr>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Email</th>
                  <th> </th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.userId}>
                    <td>{user.firstName}</td>
                    <td>{user.lastName}</td>
                    <td>{user.emailId}</td>
                    <td>
                      <Button variant="info" onClick={() => this.submitAddFriendAuto(user.userId)}>Add</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
                            
                            <Row>&nbsp;</Row>
                            <Row>&nbsp;</Row>
                            <Row>
                                {/* &nbsp;<Button color="primary" onClick={() => this.searchAutoComplete()}> Search </Button>
                                &nbsp;<Button color="primary"
                                              onClick={() => this.closeAddFriendModal()}> Close </Button> */}
                            </Row>
                        </Container>
                    </div>
                </Modal>
            </div>

        )
    }

    
    openAddFriendModal() {

        this.setState({
            addFriendPopup: true
        });

    }

    closeAddFriendModal() {
        this.setState({
            addFriendPopup: false
        });
    }

    // addFriendChange(event) {
    //     const name = event.target.name;
    //     const value = event.target.value;

    //     this.setState(state => {
    //         if (name == "firstName")
    //             state.addSearch.firstName = value
    //         else if (name == "lastName")
    //             state.addSearch.lastName = value
    //         else (name == "email")
    //         state.addSearch.email = value

    //         return state
    //     })

    // }
    
    // need to add state.addSearch.autoCompleteLoaded
    addFriendChange(event) {
        const name = event.target.name;
        const value = event.target.value;

        this.setState(state => {
            if (name == "firstName")
                state.addSearch.firstName = value
            else if (name == "lastName")
                state.addSearch.lastName = value
            else if (name == "emailId")
                state.addSearch.email = value

            state.addSearch.autoCompleteLoaded = false;

            return state
        })
    }

    searchAutoComplete() {
        var api_url = 'http://cs411ccsquad.web.illinois.edu/read/UserAuto/';
        var filters = {
                        userId: this.state.user[0].userId,
                        firstName: this.state.addSearch.firstName,
                        lastName: this.state.addSearch.lastName,
                        emailId: this.state.addSearch.email
                        }
        var filter_uri = encodeURI(JSON.stringify(filters));
        
        api_url += filter_uri;
        
        console.log(api_url);
        console.log(JSON.stringify(filters));


        if(!this.state.addSearch.autoCompleteLoaded){
            fetch(api_url)
                .then(res => res.json())
                .then(
                    (result) => {
                                    console.log(result);
                                    this.setState(state => {
                                    state.addSearch.autoCompleteLoaded = true;
                                    state.addSearch.displayUsers = result.data;
                                    return state
                                    })
                                },
                    (error) => {
                                    this.setState(state => {
                                    state.addSearch.autoCompleteLoaded = true;
                                    state.addSearch.displayUsers = [];
                                    return state
                                });
                    }
                )
        }
    }

    submitAddFriend() {
        var api_url = 'http://cs411ccsquad.web.illinois.edu/api/';

        var firstName = this.state.addSearch.firstName
        var lastName = this.state.addSearch.lastName
        var email = this.state.addSearch.email
        var filters = "select * from User where firstName = '" + firstName + "' and lastName = '" + lastName + "' and emailId = '" + email + "'"
        
        api_url = api_url + filters
        // console.log(api_url)

        fetch(api_url)
            .then(res => res.json())
            .then(
                (result) => {
                    let old_user = this.state.user
                    var result = {
                        'userId': this.state.userId,
                        'firstName': firstName,
                        'lastName': lastName,
                        'openness': result.data[0].trOpen,
                        'conscience': result.data[0].trCon,
                        'extroversion': result.data[0].trEx,
                        'agreeableness': result.data[0].trAg,
                        'neuroticism': result.data[0].trNe,
                        isMaster: 0,
                        'userRank': this.state.nextUserRank
                    };
                    this.setState({nextUserRank: this.state.nextUserRank + 1});

                    old_user.push(result);
                    this.forceUpdate()
                },
                (error) => {
                    this.setState({error})
                }
            )

    }

    submitAddFriendAuto(add_user_id){
        var api_url = 'http://cs411ccsquad.web.illinois.edu/read/User/';
        var filters = {userId: add_user_id};
        var filter_uri = encodeURI(JSON.stringify(filters));
        api_url += filter_uri;

        fetch(api_url)
            .then(res => res.json())
            .then(
                (result) => {
                    let old_user = this.state.user
                    var result = {
                        'userId': result.data[0].userId,
                        'firstName': result.data[0].firstName,
                        'lastName': result.data[0].lastName,
                        'trOpen': result.data[0].trOpen,
                        'trCon': result.data[0].trCon,
                        'trEx': result.data[0].trEx,
                        'trAg': result.data[0].trAg,
                        'trNe': result.data[0].trNe,
                        isMaster: 0,
                        'userRank': this.state.nextUserRank
                    };
                    this.setState({nextUserRank: this.state.nextUserRank + 1});

                    old_user.push(result);
                    console.log(this.state.user);
                    this.forceUpdate()
                },
                (error) => {
                    this.setState({error})
                }
            )
    }
    deleteFriendPopup() {
        return (

            <div>
                <Button color="primary" onClick={() => this.openDeleteFriendModal()}> Delete Friend from Chart</Button>
                <Modal visible={this.state.deleteFriendPopup} width="800" height="800" effect="fadeInUp"
                       onClickAway={() => this.closeDeleteFriendModal()}>
                    <div>
                        <h1>&nbsp;Delete Friend from Chart</h1>
                        <Container>

                            <Table>
                                <thead>
                                <tr>
                                    <th>First Name</th>
                                    <th>Last Name</th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.state.user.map(u => (
                                    <tr key={u.userRank}>
                                        <td>{u.firstName}</td>
                                        <td>{u.lastName}</td>
                                        <td>
                                            <Button color="primary" disabled={Boolean(u.isMaster)}
                                                    onClick={() => this.submitDeleteFriend(u.userRank)}>Delete</Button>
                                        </td>
                                    </tr>
                                ))}
                                </tbody>
                            </Table>

                            <Row>
                                &nbsp;<Button color="primary"
                                              onClick={() => this.closeDeleteFriendModal()}> Close </Button>
                            </Row>
                        </Container>
                    </div>
                </Modal>
            </div>

        )
    }

    openDeleteFriendModal() {
        this.setState({
            deleteFriendPopup: true
        });
    }

    closeDeleteFriendModal() {
        this.setState({
            deleteFriendPopup: false
        });
    }

    submitDeleteFriend(id) {

        this.setState(state => {
            const user = state.user.filter(function (u) {
                return u.userRank != id
            });

            return {user};
        })
    }

    navtoCRUDAMovies(){
        
        var usertoCURD = Object.assign({}, this.state.user[0]);
        usertoCURD["database"] = 0;
        
        ReactDOM.unmountComponentAtNode(document.getElementById('root'));     
        ReactDOM.render(<CRUDApp  usertoCURD = {usertoCURD}/>, document.getElementById('root'));
                
    }

    navtoCRUDACocktails(){

        var usertoCURD = Object.assign({}, this.state.user[0]);
        usertoCURD["database"] = 1;
        
        ReactDOM.unmountComponentAtNode(document.getElementById('root'));     
        ReactDOM.render(<CRUDApp usertoCURD = {usertoCURD}/>, document.getElementById('root'));
    }

    render() {
        this.getTopGenres();
        return (

            <div>
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand href="">Flicks n Drinks</Navbar.Brand>
                    <Nav className="mr-auto">
                        <Button variant="dark"> My profile </Button>
                        <Button variant="dark"   onClick={() => this.navtoCRUDAMovies()}> Movies</Button>
                        <Button variant="dark"  onClick={() => this.navtoCRUDACocktails()}> Cocktails </Button>
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
                        <Col>&nbsp;</Col>
                        <Col><h2> Hi, {this.state.user[0].firstName} {this.state.user[0].lastName} </h2></Col>
                        <Col>&nbsp;</Col>
                    </Row>

                    <Row><br/><br/><br/></Row>

                    <Row>
                        <Col sm={3}>
                            <Row>
                                <OverlayTrigger trigger="click" placement="right" overlay={
                                    <Popover id="popover-basic">
                                        <Popover.Title as="h3">Personality Traits</Popover.Title>
                                        <Popover.Content>
                                            <strong>Openness</strong><br />
                                            A <strong>High</strong> value means that you are very creative, try new things and tackle new challenges.<br/>
                                            A <strong>Low</strong> value means that you are not so creative, don't try new things and don't like new challenges.<br/>
                                            <br />
                                            <strong>Conscientiousness</strong><br />
                                            A <strong>High</strong> value means that you like setting schedules, prioritize work and pay attention to detail.<br/>
                                            A <strong>Low</strong> value means that you do not enjoy setting schedules, don't prioritize work and are not so attentive.<br/>
                                            <br />
                                            <strong>Extraversion</strong><br />
                                            A <strong>High</strong> value means that you are very gregarious, energetic and straight forward.<br/>
                                            A <strong>Low</strong> value means that you are shy, less energetic and enjoy being alone.<br/>
                                            <br />
                                            <strong>Agreeableness</strong><br />
                                            A <strong>High</strong> value means that you are helpful, caring and empathetic towards people.<br/>
                                            A <strong>Low</strong> value means that you are disinterested and not concerned for other people.<br/>
                                            <br />
                                            <strong>Neuroticism</strong><br />
                                            A <strong>High</strong> value means that you get anxious or upset easily and experience dramatic mood swings.<br/>
                                            A <strong>Low</strong> value means that you remain calm and composed in difficult situations.<br/>
                                        </Popover.Content>
                                    </Popover>
                                }>
                                    <Button variant="dark">Personality Traits - Click Me!</Button>
                                </OverlayTrigger>
                            </Row>
                            <Row>&nbsp;</Row>
                            <Row>
                                <a href="https://www.truity.com/view/tests/big-five-personality">Take Personality Test</a>
                            </Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Openness: {this.state.user[0].trOpen}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].trOpen} onChange={(e) => {
                                this.handleChange_Openness(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Conscientiousness:{this.state.user[0].trCon}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].trCon} onChange={(e) => {
                                this.handleChange_Conscientiousness(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Extroversion: {this.state.user[0].trEx}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].trEx} onChange={(e) => {
                                this.handleChange_Extroversion(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Agreeableness: {this.state.user[0].trAg}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].trAg} onChange={(e) => {
                                this.handleChange_Agreeableness(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Neuroticism: {this.state.user[0].trNe}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].trNe} onChange={(e) => {
                                this.handleChange_Neuroticism(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row>{this.submitPersonalityChange()}</Row>
                            <Row>&nbsp;</Row>
                            <Row>&nbsp;</Row>
                            <Row>{<TopGenres genres={this.state.topGenres}/>}</Row>

                        </Col>

                        <Col sm={9}>

                            <Row>
                                <Col>
                                    {this.showChart()}
                                </Col>
                            </Row>

                            <Row>
                                <Col></Col>{this.addFriendPopup()} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {this.deleteFriendPopup()}<Col></Col>
                            </Row>

                        </Col>

                    </Row>

                </Container>
            </div>
        );
    }
}

export default UserApp;
