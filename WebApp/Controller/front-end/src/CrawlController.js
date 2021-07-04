import React, { Component } from 'react';
import { Table }            from 'react-bootstrap';
import {Modal, Row, Col, Form, Button, Dropdown} from 'react-bootstrap';

import { ButtonToolbar }    from 'react-bootstrap';
import { AddNewParser }             from './AddNewParser';
import { EditParser }               from './EditParser';

export class CrawlController extends Component{

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

                <hr/>
                <Table className="mt-4" striped bordered hover size="sm">
                    <thead>
                        <tr>
                        <th>Status</th>
                        <th>Name</th>
                        <th>Infomation</th>
                        <th>Option</th>
                        </tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td>Crawling</td>
                                <td>Worker 01</td>
                                <td>Site: batdongsan.com.vn, Type: House, 11/2021-12/2021, Numpost: 221, Error: 0</td>
                                <td>
                                <ButtonToolbar>
                                    <Button className="mr-2" variant="info">
                                        Stop
                                    </Button>

                                    <Button className="mr-2" variant="danger">
                                        Cancel
                                    </Button>
                                
                                </ButtonToolbar>

                                </td>

                            </tr>
                            <tr>
                                <td>Parsing</td>
                                <td>Worker 02</td>
                                <td>Site: batdongsan.com.vn, StsParse: 0, Type: Land, 11/2021-12/2021, Numpost: 72, Error: 0</td>
                                <td>
                                <ButtonToolbar>
                                    <Button className="mr-2" variant="info">
                                        Stop
                                    </Button>

                                    <Button className="mr-2" variant="danger">
                                        Cancel
                                    </Button>
                                
                                </ButtonToolbar>

                                </td>

                            </tr>
                            
                    </tbody>

                </Table>
            </div>
        );
    }

}