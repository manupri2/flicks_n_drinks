import React, {Component} from 'react';
import {Button, Container, Col, Form, Jumbotron} from 'react-bootstrap';
import "../dist/signup-page.css"


class SignupApp extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    l(){
        alert('Test')
    }
    render() {
        return(
            <div>
                <Container>
                    <Form>
                        <h2 className="text-center">Sign Up</h2>
                        <Form.Group size="lg" controlId="formFirstName">
                            <Form.Label>First Name</Form.Label>
                            <Form.Control type="email" placeholder="Enter First Name"/>
                        </Form.Group>
                        <Form.Group size="lg" controlId="formLastName">
                            <Form.Label>Last Name</Form.Label>
                            <Form.Control type="email" placeholder="Enter Last Name"/>
                        </Form.Group>
                        <Form.Group size="lg" controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control type="email" placeholder="Enter email"/>
                        </Form.Group>
                        <Form.Group size="lg" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password"/>
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

export default SignupApp;
