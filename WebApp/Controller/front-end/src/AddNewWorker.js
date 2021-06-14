import React,{Component} from 'react';
import {Modal,Button, Row, Col, Form} from 'react-bootstrap';

export class AddNewWorker extends Component{
    constructor(props){
        super(props);
        this.handleSubmit=this.handleSubmit.bind(this);
    }

    handleSubmit(event){

        event.preventDefault();
        fetch(process.env.REACT_APP_API + 'worker/',{
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                WorkerID:null,
                WorkerName:event.target.WorkerName.value,
                WorkerIP:event.target.WorkerIP.value,
                RmqPassword:event.target.RmqPassword.value                
            })
        })
        .then(res=>res.json())
        .then((result)=>{
            alert(result);
        },
        (error)=>{
            alert(error );
        })
    }
    render(){
        return (
            <div className="container">
                <Modal
                    {...this.props}
                    size="lg"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    <Modal.Header clooseButton>
                        <Modal.Title id="contained-modal-title-vcenter">
                            Add New Worker
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>

                        <Row>
                            <Col sm={6}>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Group controlId="WorkerName">
                                        <Form.Label>Worker Name</Form.Label>
                                        <Form.Control type="text" name="WorkerName" required 
                                        placeholder="Name"/>
                                    </Form.Group>
                                    <Form.Group controlId="WorkerIP">
                                        <Form.Label>IP</Form.Label>
                                        <Form.Control type="text" name="WorkerIP" required 
                                        placeholder="172.0.0.0"/>
                                    </Form.Group>
                                    <Form.Group controlId="RmqPassword">
                                        <Form.Label>RMQ Password</Form.Label>
                                        <Form.Control type="text" name="RmqPassword" required 
                                        placeholder="Password"/>
                                    </Form.Group>
                                    <Form.Group>
                                        <Button variant="primary" type="submit">
                                            Add Department
                                        </Button>
                                    </Form.Group>
                                </Form>
                            </Col>
                        </Row>
                    </Modal.Body>
                    
                    <Modal.Footer>
                        <Button variant="danger" onClick={this.props.onHide}>Close</Button>
                    </Modal.Footer>

                </Modal>

            </div>
        )
    }

}