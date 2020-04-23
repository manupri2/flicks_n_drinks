import React, {Component} from 'react';
import {Container, Jumbotron, Alert, Form, Button, FormGroup} from 'react-bootstrap';
import {PlusCircle} from 'react-bootstrap-icons';
import "../dist/login-page.css"


class LoginApp extends Component {
    constructor(props) {
        super(props);
        this.state = {};
        this.register = this.register.bind(this);
        this.login = this.login.bind(this);
    }

    login() {

    }

    register() {

    }

    render() {

        return (
            <div>
                <Container>
                    <h2 className="text-center">Log In</h2>
                    <Form>
                        <Form.Group size="lg" controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control type="email" placeholder="Enter email"/>
                        </Form.Group>
                        <Form.Group size="lg" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password"/>
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
