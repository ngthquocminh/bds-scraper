import React,{Component} from 'react';
import {Modal,Button, Row, Col, Form} from 'react-bootstrap';

export class AddNewParser extends Component{
    constructor(props){
        super(props);
        this.handleSubmit=this.handleSubmit.bind(this);
    }

    handleSubmit(event){

        event.preventDefault();
        fetch(process.env.REACT_APP_API + 'parser/',{
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                id:null,
                site:event.target.site.value,
                features:event.target.features.value,
                default:event.target.default.value,
                xpath:event.target.xpath.value,
                pos_take:event.target.pos_take.value,
                regex_take:event.target.regex_take.value,
                regex_valid:event.target.regex_valid.value,
                len_valid:event.target.len_valid.value        
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
                                    <Form.Group controlId="site" >
                                        <Form.Label>Site</Form.Label>
                                        <Form.Control type="text" name="site" required disabled
                                        defaultValue={this.props.setName}
                                        placeholder="site"/>
                                    </Form.Group>
                                    <Form.Group controlId="features">
                                        <Form.Label>Features</Form.Label>
                                        <Form.Control type="text" name="features" required 
                                        placeholder="features name"/>
                                    </Form.Group>
                                    <Form.Group controlId="default">
                                        <Form.Label>Default</Form.Label>
                                        <Form.Control type="text" name="default"  
                                        placeholder="default"/>
                                    </Form.Group>
                                    <Form.Group controlId="xpath">
                                        <Form.Label>Xpath</Form.Label>
                                        <Form.Control type="text" name="xpath"  
                                        placeholder="Xpath"/>
                                    </Form.Group>
                                    <Form.Group controlId="pos_take">
                                        <Form.Label>Pos_take</Form.Label>
                                        <Form.Control type="text" name="pos_take"  
                                        placeholder="Pos_take"/>
                                    </Form.Group>
                                    <Form.Group controlId="pegex_take">
                                        <Form.Label>Regex_take</Form.Label>
                                        <Form.Control type="text" name="regex_take"  
                                        placeholder="Regex_take"/>
                                    </Form.Group>
                                    <Form.Group controlId="pegex_valid">
                                        <Form.Label>Regex_valid</Form.Label>
                                        <Form.Control type="text" name="regex_valid"  
                                        placeholder="Regex_valid"/>
                                    </Form.Group>
                                    <Form.Group controlId="len_valid ">
                                        <Form.Label>Len_valid</Form.Label>
                                        <Form.Control type="number" name="len_valid" required
                                        placeholder="Len_valid"/>
                                    </Form.Group>
                                    
                                    <Form.Group>
                                        <Button variant="primary" type="submit">
                                            Add
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