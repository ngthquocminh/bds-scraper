import React,{Component} from 'react';
import {Modal,Button, Row, Col, Form} from 'react-bootstrap';

export class TestWorker extends Component{
    constructor(props){
        super(props);
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
                            Trying to connect to {this.props.workerName + " - " + this.props.workerIP}
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div>
                            {this.props.response}
                        </div>                 
                    </Modal.Body>
                    
                    <Modal.Footer>
                        <Button variant="danger" onClick={this.props.onHide}>Close</Button>
                    </Modal.Footer>

                </Modal>

            </div>
        )
    }

}