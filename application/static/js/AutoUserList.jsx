import React from 'react';
import { Table, Button, Alert, Spinner } from 'react-bootstrap';

class AutoUserList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        response: {}
    }
  }

  submitAddFriend(add_user_id) {
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

// need to add state.addSearch.autoCompleteLoaded
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

            state.addSearch.autoCompleteLoaded = false;

            return state
        })
  }

// need to add state.addSearch.displayUsers
  searchAutoComplete() {
        var api_url = 'http://cs411ccsquad.web.illinois.edu/read/UserAuto/';
        var filters = {
                        userId: this.state.user[0].userId,
                        firstName: this.state.addSearch.firstName,
                        lastName: this.state.addSearch.lastName,
                        email: this.state.addSearch.email
                        }
        var filter_uri = encodeURI(JSON.stringify(filters));
        api_url += filter_uri;

            if(!this.state.addSearch.autoCompleteLoaded){
                fetch(api_url)
                    .then(res => res.json())
                    .then(
                        (result) => {
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

// set props for 'users=this.state.addSearch.displayUsers' and 'submitAddFriend=this.props.submitAddFriend'
  render() {
    const users = this.props.users;

      return(
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
                    <Button variant="info" onClick={() => this.props.submitAddFriend(user.userId)}>Add</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      )
    }
}

export default AutoUserList;
