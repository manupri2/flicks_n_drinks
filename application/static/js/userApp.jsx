import React, {Component} from 'react';
import Chart from "react-apexcharts";
import {Table, Container, Row, Col, Button, Nav, Navbar} from 'react-bootstrap';
import Modal from 'react-awesome-modal';
import ReactDOM from 'react-dom';
import CRUDApp from './CRUDApp';
import TopGenres from './TopGenres';


class UserApp extends Component {
    constructor(props) {
        super(props);

        let defaultUser =
            this.props.userDetails == null ? {
                    userId: 2,
                    firstName: 'Oscar',
                    lastName: 'Huang',
                    openness: 80,
                    agreeableness: 40,
                    neuroticism: 100,
                    extroversion: 30,
                    conscience: 50,
                    isMaster: 1,
                    userRank: 0
                } :

                {
                    userId: this.props.userDetails.userId,
                    firstName: this.props.userDetails.firstName,
                    lastName: this.props.userDetails.lastName,
                    openness: this.props.userDetails.trOpen,
                    agreeableness: this.props.userDetails.trAg,
                    neuroticism: this.props.userDetails.trNe,
                    extroversion: this.props.userDetails.trEx,
                    conscience: this.props.userDetails.trCon,
                    isMaster: 1,
                    userRank: 0
                };

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
            addSearch: {firstName: '', lastName: '', email: ''},
            nextUserRank: 2
        }

        this.showChart = this.showChart.bind(this)
        this.handleChange_Openness = this.handleChange_Openness.bind(this)
        this.handleChange_Conscientiousness = this.handleChange_Conscientiousness.bind(this)
        this.handleChange_Extroversion = this.handleChange_Extroversion.bind(this)
        this.handleChange_Agreeableness = this.handleChange_Agreeableness.bind(this)
        this.handleChange_Neuroticism = this.handleChange_Neuroticism.bind(this)

        this.getTopGenres = this.getTopGenres.bind(this)
        this.submitPersonalityChange = this.submitPersonalityChange.bind(this)
        // this.addFriend= this.addFriend.bind(this)
        // this.deleteFriend= this.deleteFriend.bind(this)


    }

    showChart() {

        const newSeries = []
        this.state.user.map((u) => {
            const tr_list = [u.openness, u.conscience, u.extroversion, u.agreeableness, u.neuroticism];
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

        this.setState(state => {
            const user = state.user.map((u) => {
                let data = u.openness
                if (u.isMaster == 1)
                    data = input
                return {
                    userId: u.userId,
                    firstName: u.firstName,
                    lastName: u.lastName,
                    isMaster: u.isMaster,
                    userRank: u.userRank,
                    openness: data,
                    conscience: u.conscience,
                    extroversion: u.extroversion,
                    agreeableness: u.agreeableness,
                    neuroticism: u.neuroticism
                }
            })
            return {user}
        });
    }

    handleChange_Conscientiousness(e) {
        const input = e.target.value

        this.setState(state => {
            const user = state.user.map((u) => {
                let data = u.conscience
                if (u.isMaster == 1)
                    data = input
                return {
                    userId: u.userId,
                    firstName: u.firstName,
                    lastName: u.lastName,
                    isMaster: u.isMaster,
                    userRank: u.userRank,
                    openness: u.openness,
                    conscience: data,
                    extroversion: u.extroversion,
                    agreeableness: u.agreeableness,
                    neuroticism: u.neuroticism
                }
            })
            return {user}
        });
    }

    handleChange_Extroversion(e) {
        const input = e.target.value

        this.setState(state => {
            const user = state.user.map((u) => {
                let data = u.extroversion
                if (u.isMaster == 1)
                    data = input
                return {
                    userId: u.userId,
                    firstName: u.firstName,
                    lastName: u.lastName,
                    isMaster: u.isMaster,
                    userRank: u.userRank,
                    openness: u.openness,
                    conscience: u.conscience,
                    extroversion: data,
                    agreeableness: u.agreeableness,
                    neuroticism: u.neuroticism
                }
            })
            return {user}
        });
    }

    handleChange_Agreeableness(e) {
        const input = e.target.value

        this.setState(state => {
            const user = state.user.map((u) => {
                let data = u.agreeableness
                if (u.isMaster == 1)
                    data = input
                return {
                    userId: u.userId,
                    firstName: u.firstName,
                    lastName: u.lastName,
                    isMaster: u.isMaster,
                    userRank: u.userRank,
                    openness: u.openness,
                    conscience: u.conscience,
                    extroversion: u.extroversion,
                    agreeableness: data,
                    neuroticism: u.neuroticism
                }
            })
            return {user}
        });
    }

    handleChange_Neuroticism(e) {
        const input = e.target.value

        this.setState(state => {
            const user = state.user.map((u) => {
                let data = u.neuroticism
                if (u.isMaster == 1)
                    data = input
                return {
                    userId: u.userId,
                    firstName: u.firstName,
                    lastName: u.lastName,
                    isMaster: u.isMaster,
                    userRank: u.userRank,
                    openness: u.openness,
                    conscience: u.conscience,
                    extroversion: u.extroversion,
                    agreeableness: u.agreeableness,
                    neuroticism: data
                }
            });
            return {user}
        });
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
        let open = this.state.user[0].openness;
        let con = this.state.user[0].conscience;
        let ext = this.state.user[0].extroversion;
        let agr = this.state.user[0].agreeableness;
        let neu = this.state.user[0].neuroticism;
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

        console.log(this.state.editPersonalityResult)

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

        return (

            <div>
                <Button color="primary " onClick={() => this.openAddFriendModal()}> Add Friend </Button>
                <Modal visible={this.state.addFriendPopup} width="800" height="400" effect="fadeInUp"
                       onClickAway={() => this.closeAddFriendModal()}>
                    <div>
                        <h1>&nbsp;Adding Friend to Chart</h1>
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
                                        &nbsp;<input type="text" name={'email'} placeholder="email"
                                                     onChange={() => this.addFriendChange(event)}/>
                                    </Row>
                                </Col>
                            </Row>
                            <Row>&nbsp;</Row>
                            <Row>&nbsp;</Row>
                            <Row>
                                &nbsp;<Button color="primary" onClick={() => this.submitAddFriend()}> Add </Button>
                                &nbsp;<Button color="primary"
                                              onClick={() => this.closeAddFriendModal()}> Close </Button>
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

    addFriendChange(event) {
        const name = event.target.name;
        const value = event.target.value;

        this.setState(state => {
            if (name == "firstName")
                state.addSearch.firstName = value
            else if (name == "lastName")
                state.addSearch.lastName = value
            else (name == "email")
            state.addSearch.email = value

            return state
        })

    }

    submitAddFriend() {
        var api_url = 'http://cs411ccsquad.web.illinois.edu/api/';

        var firstName = this.state.addSearch.firstName
        var lastName = this.state.addSearch.lastName
        var email = this.state.addSearch.email
        var filters = "select * from User where firstName = '" + firstName + "' and lastName = '" + lastName + "' and emailId = '" + email + "'"
        api_url = api_url + filters

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
        
        var usertoCURD = {
            'userId': this.state.user[0].userId,
            'firstName': this.state.user[0].firstName,
            'lastName': this.state.user[0].lastName,
            'openness': this.state.user[0].openness,
            'agreeableness': this.state.user[0].agreeableness,
            'neuroticism': this.state.user[0].neuroticism,
            'extroversion': this.state.user[0].extroversion,
            'conscience': this.state.user[0].conscience,
            'isMaster': 1,
            'userRank': 0,
            'database':"Movies"

        };

        ReactDOM.unmountComponentAtNode(document.getElementById('root'));     
        ReactDOM.render(<CRUDApp  userId={this.state.user[0].userId} />, document.getElementById('root'));
        

        
    }

    navtoCRUDACocktails(){
        ReactDOM.unmountComponentAtNode(document.getElementById('root'));     
        ReactDOM.render(<CRUDApp userId = {-1*this.state.user[0].userId}/>, document.getElementById('root'));
    }

    render() {
        this.getTopGenres();
        return (

            <div>
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand href="">Flicks n Drinks</Navbar.Brand>
                    <Nav className="mr-auto">
                        <Button variant="dark"> My profile </Button>
                        <Button variant="dark"  onClick={() => this.navtoCRUDAMovies()}> Movies </Button>
                        <Button variant="dark"  onClick={() => this.navtoCRUDACocktails()}> Cocktails </Button>
                    </Nav>  
                    <Nav className="justify-content-end" activeKey="">
                        <Nav.Item>
                            <Nav.Link href="/login">Logout</Nav.Link>
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

                            <Row><h6>Openness: {this.state.user[0].openness}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].openness} onChange={(e) => {
                                this.handleChange_Openness(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Conscientiousness:{this.state.user[0].conscience}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].conscience} onChange={(e) => {
                                this.handleChange_Conscientiousness(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Extroversion: {this.state.user[0].extroversion}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].extroversion} onChange={(e) => {
                                this.handleChange_Extroversion(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Agreeableness: {this.state.user[0].agreeableness}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].agreeableness} onChange={(e) => {
                                this.handleChange_Agreeableness(e)
                            }}></input></Row>
                            <Row>&nbsp;</Row>
                            <Row><h6>Neuroticism: {this.state.user[0].neuroticism}</h6></Row>
                            <Row><input type="range" value={this.state.user[0].neuroticism} onChange={(e) => {
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
