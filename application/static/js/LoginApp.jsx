import React, {Component, useState} from 'react';
import {Container, Jumbotron, Alert, Form, Button, FormGroup} from 'react-bootstrap';
import {PlusCircle} from 'react-bootstrap-icons';
import "../dist/login-page.css"


class LoginApp extends Component {
    constructor(props) {
        super(props);
        this.state = {
            database: "User",
            isLoggedIn: false,
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
        if(!this.state.isLoggedIn){
            fetch(apiUrl)
                .then(res => res.json())
                .then((result) => {
                            console.log("Result!!!!!!!");
                            if (result.status === 'Results found')
                                alert('Valid User');
                            else
                                alert('Invalid User');
                            },
                        (error) => {
                            console.log("Error!!!!!!!!!");
                            console.log(error.message);
                        } )

        }

    }


    render() {

        return (
            <div>
                <Container>
                    <Form onSubmit={this.handleSubmit}>
                        <h2 className="text-center">Log In</h2>
                        <Form.Group size="lg" controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control
                                required
                                type="email"
                                name="email"
                                value={this.state.email}
                                onChange={this.handleChange}
                                placeholder="Enter email" />
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
                        <Button variant="success" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Container>
            </div>
        );
    }
}

export default LoginApp;
