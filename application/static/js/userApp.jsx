import React, {Component} from 'react';
import Chart from "react-apexcharts";
import { Table, Container, Row, Col, Button} from 'reactstrap';
import Modal from 'react-awesome-modal';

class userApp extends Component {
  constructor(props) {
    super(props);

    
    this.state = {
      user:[{
        userId:0,
        firstName:'Oscar',
        lastName:'Huang',
        data: [80,50,30,40,100],
        isMaster: 1,
        userRank :0
      },
      {
        userId:1,
        firstName:'Barney',
        lastName:'Stinson',
        data: [100,20,80,90,10],
        isMaster: 0,
        userRank :1
      }
    ],

      chart:{
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
            labels:{
              style: {
                fontSize: '14px'
              }
            }
          },
          yaxis:{
            min:0,
            max:100,
            tickAmount: 5,
            
          }
        },

      },

      addFriendPopup:false,
      deleteFriendPopup:false,
      editPersonalityPopup: false,
      editPersonalityResult: '',
      addSearch:{firstName:'', lastName:'', email:''},
      nextUserRank:2
    }

    this.showChart= this.showChart.bind(this)
    this.handleChange_Openness= this.handleChange_Openness.bind(this)
    this.handleChange_Conscientiousness= this.handleChange_Conscientiousness.bind(this)
    this.handleChange_Extroversion= this.handleChange_Extroversion.bind(this)
    this.handleChange_Agreeableness= this.handleChange_Agreeableness.bind(this)
    this.handleChange_Neuroticism= this.handleChange_Neuroticism.bind(this)

    this.submitPersonalityChange= this.submitPersonalityChange.bind(this)    
    // this.addFriend= this.addFriend.bind(this)
    // this.deleteFriend= this.deleteFriend.bind(this)


  }


  showChart(){
    
    const newSeries = []
    this.state.user.map((u) =>{
      const data = u.data.map((tr) => {return tr})
      newSeries.push({data, name:u.firstName + ' ' + u.lastName })
    })
    
    return(
    <Chart
          options={this.state.chart.options}
          series={newSeries}
          type = "radar"
          width = "800px"
          height = "600px"

          />
    )   
  }


  handleChange_Openness(e){
    const input = e.target.value
    
    this.setState(state => {
      const user = state.user.map ((u) =>{
        const data = u.data.map((d) => {return d})
        if(u.isMaster ==1)
          data[0] = input
        return {userId:u.userId, firstName: u.firstName, lastName: u.lastName, isMaster: u.isMaster,data, userRank:u.userRank}
      })
      return {user}
    });
  }

  handleChange_Conscientiousness(e){
    const input = e.target.value
    
    this.setState(state => {
      const user = state.user.map ((u) =>{
        const data = u.data.map((d) => {return d})
        if(u.isMaster ==1)
          data[1] = input
        return {userId:u.userId, firstName: u.firstName, lastName: u.lastName, isMaster: u.isMaster,data, userRank:u.userRank}
      })
      return {user}
    });
  }

  handleChange_Extroversion(e){
    const input = e.target.value
    
    this.setState(state => {
      const user = state.user.map ((u) =>{
        const data = u.data.map((d) => {return d})
        if(u.isMaster ==1)
          data[2] = input
        return {userId:u.userId, firstName: u.firstName, lastName: u.lastName, isMaster: u.isMaster,data, userRank:u.userRank}
      })
      return {user}
    });
  }

  handleChange_Agreeableness(e){
    const input = e.target.value
    
    this.setState(state => {
      const user = state.user.map ((u) =>{
        const data = u.data.map((d) => {return d})
        if(u.isMaster ==1)
          data[3] = input
        return {userId:u.userId, firstName: u.firstName, lastName: u.lastName, isMaster: u.isMaster,data, userRank:u.userRank}
      })
      return {user}
    });
  }

  handleChange_Neuroticism(e){
    const input = e.target.value
    
    this.setState(state => {
      const user = state.user.map ((u) =>{
        const data = u.data.map((d) => {return d})
        if(u.isMaster ==1)
          data[4] = input
        return {userId:u.userId, firstName: u.firstName, lastName: u.lastName, isMaster: u.isMaster,data, userRank:u.userRank}
      })
      return {user}
    });
  }


  submitPersonalityChange(){
    
    return(
      <div>
        <Button onClick={() => this.openEditModal()}>Submit Change</Button>
        <Modal visible={this.state.editPersonalityPopup} width="800" height="400" effect="fadeInUp" onClickAway={() => this.closeEditModal()}>
            <h2>&nbsp;&nbsp;{this.state.editPersonalityResult.message}</h2>
            <br/><br/><br/><br/><br/>
            &nbsp;&nbsp;<Button onClick={() => this.closeEditModal()}> Close </Button>
        </Modal>              
      </div>
    )

  }

  openEditModal(){
    this.setState({
      editPersonalityPopup : true
    });

    var api_url = 'http://cs411ccsquad.web.illinois.edu/edit/User/';
    api_url += this.state.user[0].userId +'/'
    
    for(const [index, value] of this.state.user[0].data.entries()){
      api_url += value+":"
    }
    
    fetch(api_url)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({editPersonalityResult:result})
        },
        (error) => {this.setState({error})}
      )
      
      console.log(this.state.editPersonalityResult)

  }

  closeEditModal(){
    this.setState({
      editPersonalityPopup : false
    });
  }

  addFriendPopup(){

    return (
    
    <div>
    <Button onClick={() => this.openAddFriendModal()}> Add Friend </Button>
    <Modal visible={this.state.addFriendPopup} width="800" height="400" effect="fadeInUp" onClickAway={() => this.closeAddFriendModal()}>
        <div>
            <h1>&nbsp;Adding Friend to Chart</h1>
            <Container>
            <Row>&nbsp;</Row>
            <Row>&nbsp;</Row>
              <Row>
              <Col sm={4}>
                <Row>&nbsp;<h4>First Name</h4></Row>
                <Row>
                  &nbsp;<input type="text" name = {'firstName'} placeholder="first name" onChange={() => this.addFriendChange(event)}/>
                </Row>
              </Col>

              <Col sm={4}>
                <Row>&nbsp;<h4>Last Name</h4></Row>
                <Row>
                  &nbsp;<input type="text" name = {'lastName'} placeholder="last name" onChange={() => this.addFriendChange(event)}/>
                </Row>
              </Col>

              <Col sm={4}>
                <Row>&nbsp;<h4>Email</h4></Row>
                <Row>
                  &nbsp;<input type="text" name = {'email'} placeholder="email" onChange={() => this.addFriendChange(event)}/>
                </Row>
              </Col>
              </Row>
              <Row>&nbsp;</Row>
              <Row>&nbsp;</Row>
            <Row>
            &nbsp;<Button onClick={() => this.submitAddFriend()}> Add </Button>
            &nbsp;<Button onClick={() => this.closeAddFriendModal()}> Close </Button>
            </Row>
            </Container>
        </div>
    </Modal>
    </div>

    )
  }

  openAddFriendModal() {

    
    this.setState({
      addFriendPopup : true
    });

  } 

  closeAddFriendModal() {
      this.setState({
        addFriendPopup : false
      });
  }

  addFriendChange(event){
    const name = event.target.name;
    const value = event.target.value;

    this.setState(state =>{
      if(name == "firstName")
        state.addSearch.firstName = value
      else if(name == "lastName")
        state.addSearch.lastName = value
      else (name == "email")
        state.addSearch.email = value

      return state
    })

  }


  submitAddFriend(){
    var api_url = 'http://cs411ccsquad.web.illinois.edu/api/';
    
    var firstName = this.state.addSearch.firstName
    var lastName = this.state.addSearch.lastName
    var email = this.state.addSearch.email
    var filters = "select * from User where firstName = '" + firstName +"' and lastName = '" + lastName + "' and emailId = '" + email + "'"
    api_url = api_url + filters

    fetch(api_url)
      .then(res => res.json())
      .then(
        (result) => {
          let old_user = this.state.user
          var result = {'userId':this.state.userId, 'firstName': firstName, 'lastName':lastName, 
                        'data':[result.data[0].trOpen,result.data[0].trCon,result.data[0].trEx,result.data[0].trAg,result.data[0].trNe], isMaster:0,
                        'userRank':this.state.nextUserRank}
          this.setState({nextUserRank: this.state.nextUserRank+1});

          old_user.push(result)
          console.log(this.state.user)
          this.forceUpdate()
        },
        (error) => {this.setState({error})}
      )
    
  }


  deleteFriendPopup(){
    return (
    
    <div>
    <Button onClick={() => this.openDeleteFriendModal()}> Delete Friend from Chart</Button>
    <Modal visible={this.state.deleteFriendPopup} width="800" height="800" effect="fadeInUp" onClickAway={() => this.closeDeleteFriendModal()}>
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
                <tr key = {u.userRank}>
                  <td>{u.firstName}</td>
                  <td>{u.lastName}</td>
                  <td>                    
                     <Button disabled={Boolean(u.isMaster)} onClick = {()=>this.submitDeleteFriend(u.userRank)}>Delete</Button> 
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          
            <Row>
            &nbsp;<Button onClick={() => this.closeDeleteFriendModal()}> Close </Button>
            </Row>
            </Container>
        </div>
    </Modal>
    </div>

    )
  }

  openDeleteFriendModal() {
    this.setState({
      deleteFriendPopup : true
    });
  } 

  closeDeleteFriendModal() {
      this.setState({
        deleteFriendPopup : false
      });
  }

  submitDeleteFriend(id){
 
    this.setState(state => {
      const user = state.user.filter(function(u){
        return u.userRank != id
      });
    
    return {user};
    })
  }
  
  render() {

    return (
    

    <Container>
      <br/><br/><br/>
      
    
      <Row>
        <Col>&nbsp;</Col>
        <Col><h2> Hi, {this.state.user[0].firstName} {this.state.user[0].lastName} </h2></Col>
        <Col>&nbsp;</Col>
      </Row>
        
      <Row><br/><br/><br/></Row>
        
      <Row>
        <Col sm={3}>

          <Row><h6>Openness: {this.state.user[0].data[0]}</h6></Row>
          <Row><input type = "range" value= {this.state.user[0].data[0]} onChange={(e) => {this.handleChange_Openness(e)}}></input></Row>
          <Row>&nbsp;</Row>
          <Row><h6>Conscientiousness:{this.state.user[0].data[1]}</h6></Row>
          <Row><input type = "range" value= {this.state.user[0].data[1]} onChange={(e) => {this.handleChange_Conscientiousness(e)}}></input></Row>
          <Row>&nbsp;</Row>
          <Row><h6>Extroversion: {this.state.user[0].data[2]}</h6></Row>
          <Row><input type = "range" value= {this.state.user[0].data[2]} onChange={(e) => {this.handleChange_Extroversion(e)}}></input></Row>
          <Row>&nbsp;</Row>
          <Row><h6>Agreeableness: {this.state.user[0].data[3]}</h6></Row>
          <Row><input type = "range" value= {this.state.user[0].data[3]} onChange={(e) => {this.handleChange_Agreeableness(e)}}></input></Row>
          <Row>&nbsp;</Row>
          <Row><h6>Neuroticism: {this.state.user[0].data[4]}</h6></Row>
          <Row><input type = "range" value= {this.state.user[0].data[4]} onChange={(e) => {this.handleChange_Neuroticism(e)}}></input></Row>
          <Row>&nbsp;</Row>
          <Row>{this.submitPersonalityChange()}</Row>
        
        </Col>

        <Col sm={9}>

          <Row>{this.showChart()}</Row>

          <Row> <Col></Col>{this.addFriendPopup()} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {this.deleteFriendPopup()}<Col></Col></Row>
          
        </Col>

      </Row>

    </Container>
      
    );
  }
}

export default userApp;