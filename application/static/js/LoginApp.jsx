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
            email: '',
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

        const form = event.currentTarget;
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }

        setValidated(true);

        let db = this.state.database;
        let apiUrl = 'http://cs411ccsquad.web.illinois.edu/';
        let email = encodeURI(JSON.stringify(this.state.email));
        apiUrl += db + "/" + email;
        if(!this.state.isLoggedIn){
            fetch(apiUrl)
                .then((res => res.json()))
                .then((result) =>{
                    console.log(result);
                    if (result.status === 'Invalid')
                        alert('Invalid User');
                    else
                    this.props.history.push("/CRUDpage.html");
                })
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
                        <Form.Control.Feedback type="invalid">Please enter email address.</Form.Control.Feedback>
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
                            <Form.Control.Feedback type="invalid">Please enter password.</Form.Control.Feedback>
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
