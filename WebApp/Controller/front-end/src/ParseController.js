import React, { Component } from 'react';
import { Table }            from 'react-bootstrap';
import {Modal, Row, Col, Form, Button, Dropdown} from 'react-bootstrap';

import { ButtonToolbar }    from 'react-bootstrap';
import { AddNewParser }             from './AddNewParser';
import { EditParser }               from './EditParser';

export class ParseController extends Component{

    constructor(props){
        super(props);
        this.state={set_name:"bat-dong-san-com-vn"}
    }

    refreshList(){

    }

    componentDidMount(){
        this.refreshList();
    }

    componentDidUpdate(){
        this.refreshList();
    }

    handleSubmit(event) {

    }

    render(){
        const {set_name}=this.state;

        return(
            <div className="container">
                <Button 
                variant="info"
                onClick={(event)=>this.setState({set_name:"bat-dong-san-com-vn"})}
                >
                    batdongsan.com.vn
                </Button>
                <hr/>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group>
                        <Dropdown>
                            <Dropdown.Toggle variant="success" id="dropdown-basic">
                                Nhà
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                <Dropdown.Item href="#/nha">Nhà</Dropdown.Item>
                                <Dropdown.Item href="#/dat">Đất</Dropdown.Item>
                                <Dropdown.Item href="#/chung-cu">Chung cư</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        <Button variant="primary" type="submit">
                            Start CRAWL
                        </Button>
  
                    </Form.Group>
                    <Form.Group>
                        <Dropdown>
                            <Dropdown.Toggle variant="success" id="dropdown-basic">
                                Nhà
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                <Dropdown.Item href="#/nha">Nhà</Dropdown.Item>
                                <Dropdown.Item href="#/dat">Đất</Dropdown.Item>
                                <Dropdown.Item href="#/chung-cu">Chung cư</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        <Button variant="primary" type="submit">
                            Start PARSE
                        </Button>
  
                    </Form.Group>
                </Form>
            </div>
        );
    }

}