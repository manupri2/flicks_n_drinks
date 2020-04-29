import React, {Component} from 'react';
import {Button, Container, Col, Form, Jumbotron} from 'react-bootstrap';
import "../dist/signup-page.css"
import ReactDOM from "react-dom";
import CRUDApp from "./CRUDApp";
import LoginApp from "./LoginApp";


class SignupApp extends Component {
    constructor(props) {
        super(props);
        this.state = {
            database: "User",
            firstName:'',
            lastName:'',
            email:'',
            password:'',
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
        var apiUrl = 'http://cs411ccsquad.web.illinois.edu/add/';
        console.log("Url " + apiUrl);
        var body = encodeURI(JSON.stringify({
            'firstName': this.state.firstName,
            'lastName': this.state.lastName,
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
                        if (result.status === 'success'){
                            ReactDOM.unmountComponentAtNode(document.getElementById('signup'));
                            ReactDOM.render(<LoginApp />, document.getElementById('signup'));
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
        return(
            <div>
                <Container>
                    <Form onSubmit={this.handleSubmit}>
                        <h2 className="text-center">Sign Up</h2>
                        <Form.Group size="lg" controlId="formFirstName">
                            <Form.Label>First Name</Form.Label>
                            <Form.Control
                                required
                                type="text"
                                name="firstName"
                                value={this.state.firstName}
                                onChange={this.handleChange}
                                placeholder="Enter First Name"/>
                        </Form.Group>
                        <Form.Group size="lg" controlId="formLastName">
                            <Form.Label>Last Name</Form.Label>
                            <Form.Control
                                required
                                type="text"
                                name="lastName"
                                value={this.state.lastName}
                                onChange={this.handleChange}
                                placeholder="Enter Last Name"/>
                        </Form.Group>
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
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Container>
            </div>
        );
    }
}

export default SignupApp;
