import React, {Component, useState} from 'react';
import {Container, Jumbotron, Alert, Form, Button, FormGroup} from 'react-bootstrap';
import {PlusCircle} from 'react-bootstrap-icons';
import ReactDOM from 'react-dom';
import "../dist/login-page.css"
import UserApp from './userApp';



class LoginApp extends Component {
    constructor(props) {
        super(props);
        this.state = {
            database: "User",
            isLoggedIn: false,
            email: '',
            password: '',
            setValidated: false
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        const name = event.target.name;
        const value = event.target.value;

        this.setState({
            [name]: value
        })
    }

    handleSubmit(event) {
        event.preventDefault();
        var db = this.state.database;
        var apiUrl = 'http://cs411ccsquad.web.illinois.edu/read/';
        console.log("Url " + apiUrl);
        var body = encodeURI(JSON.stringify({
            'emailId': this.state.email,
            'password': this.state.password
        }));
        console.log("Url " + apiUrl);
        apiUrl += db + "/" + body;
        console.log("Url " + apiUrl);
        if (!this.state.isLoggedIn) {
            fetch(apiUrl)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then((result) => {
                        console.log("Result!!!!!!!");
                        if (result.status === 'Results found'){

                            ReactDOM.unmountComponentAtNode(document.getElementById('root'));
                            ReactDOM.render(<UserApp userDetails={result.data[0]}/>, document.getElementById('root'));
                        }
                        else
                            alert('Invalid User');
                    },
                    (error) => {
                        console.log("Error!!!!!!!!!");
                        console.log(error);
                    })
                .catch((error)=> { 
                    console.log(error)
                 });
        }
        this.setState(this.state);
    }


    render() {
        const loginFormStyle = {
              width: "420px",
              height: "480px",
              position: "relative",
              margin: "5% auto",
              backgroundColor: "#fff",
              padding: "5px",
              overflow: "hidden",
              border: "2px solid #000"
        };
        return (
            <div>
                <Container>
                    <Form style={loginFormStyle} onSubmit={this.handleSubmit}>
                        <h2 className="text-center">Log In</h2>
                        <Form.Group size="lg" controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control
                                required
                                type="email"
                                name="email"
                                value={this.state.email}
                                onChange={this.handleChange}
                                placeholder="Enter email"/>
                        </Form.Group>
                        <Form.Group size="lg" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                required
                                type="password"
                                name="password"
                                value={this.state.password}
                                onChange={this.handleChange}
                                placeholder="Password"/>
                        </Form.Group>
                        <Form.Group size="md" controlId="formBasicCheckbox">
                            <Form.Check type="checkbox" label="Remember Password"/>
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Container>
            </div>
        );
    }
}

export default LoginApp;
