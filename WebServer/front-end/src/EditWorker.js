import React,{Component} from 'react';
import {Modal,Button, Row, Col, Form} from 'react-bootstrap';

export class EditWorker extends Component{
    constructor(props){
        super(props);
        this.handleSubmit=this.handleSubmit.bind(this);
    }

    handleSubmit(event){
        event.preventDefault();
        fetch(process.env.REACT_APP_API+'worker/',{
            method:'PUT',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                WorkerID:event.target.WorkerID.value,
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
            alert('Failed');
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
    <Modal.Header>
        <Modal.Title id="contained-modal-title-vcenter">
            Edit Worker
        </Modal.Title>
    </Modal.Header>
    <Modal.Body>

        <Row>
            <Col sm={6}>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId="WorkerID">
                        <Form.Label>Worker ID</Form.Label>
                        <Form.Control type="text" name="WorkerID" required 
                        disabled
                        defaultValue={this.props.workerID}
                        placeholder="ID"/>
                    </Form.Group>
                    <Form.Group controlId="WorkerName">
                        <Form.Label>Worker Name</Form.Label>
                        <Form.Control type="text" name="WorkerName" required 
                        defaultValue={this.props.workerName}
                        placeholder="Name"/>
                    </Form.Group>
                    <Form.Group controlId="WorkerIP">
                        <Form.Label>IP</Form.Label>
                        <Form.Control type="text" name="WorkerIP" required 
                        defaultValue={this.props.workerIP}
                        placeholder="172.0.0.0"/>
                    </Form.Group>
                    <Form.Group controlId="RmqPassword">
                        <Form.Label>RMQ Password</Form.Label>
                        <Form.Control type="text" name="RmqPassword" required 
                        defaultValue={this.props.workerRmqPass}
                        placeholder="Password"/>
                    </Form.Group>
                    <Form.Group>
                        <Button variant="primary" type="submit">
                            Save
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