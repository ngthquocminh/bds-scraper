import React,{Component} from 'react';
import {Modal,Button, Row, Col, Form} from 'react-bootstrap';

export class EditParser extends Component{
    constructor(props){
        super(props);
        this.handleSubmit=this.handleSubmit.bind(this);
    }

    handleSubmit(event){
        event.preventDefault();

        fetch(process.env.REACT_APP_API+'parser/',{
            method:'PUT',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                id:event.target.id.value,
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
    <Modal.Header clooseButton>
        <Modal.Title id="contained-modal-title-vcenter">
            Edit Worker
        </Modal.Title>
    </Modal.Header>
    <Modal.Body>
        <Row>
            <Col sm={6}>
            <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId="id" >
                        <Form.Label>ID</Form.Label>
                        <Form.Control type="text" name="id" required disabled
                        defaultValue={this.props.editData.id}
                        placeholder="id"/>
                    </Form.Group>
                    <Form.Group controlId="site" >
                        <Form.Label>Site</Form.Label>
                        <Form.Control type="text" name="site" required disabled
                        defaultValue={this.props.editData.site}
                        placeholder="site"/>
                    </Form.Group>
                    <Form.Group controlId="features">
                        <Form.Label>Features</Form.Label>
                        <Form.Control type="text" name="features" required 
                        defaultValue={this.props.editData.features}
                        placeholder="features name"/>
                    </Form.Group>
                    <Form.Group controlId="default">
                        <Form.Label>Default</Form.Label>
                        <Form.Control type="text" name="default"  
                        defaultValue={this.props.editData.default}
                        placeholder="default"/>
                    </Form.Group>
                    <Form.Group controlId="xpath">
                        <Form.Label>Xpath</Form.Label>
                        <Form.Control type="text" name="xpath"  
                        defaultValue={this.props.editData.xpath}
                        placeholder="Xpath"/>
                    </Form.Group>
                    <Form.Group controlId="pos_take">
                        <Form.Label>Pos_take</Form.Label>
                        <Form.Control type="text" name="pos_take"  
                        defaultValue={this.props.editData.pos_take}
                        placeholder="Pos_take"/>
                    </Form.Group>
                    <Form.Group controlId="pegex_take">
                        <Form.Label>Regex_take</Form.Label>
                        <Form.Control type="text" name="regex_take"  
                        defaultValue={this.props.editData.regex_take}
                        placeholder="Regex_take"/>
                    </Form.Group>
                    <Form.Group controlId="pegex_valid">
                        <Form.Label>Regex_valid</Form.Label>
                        <Form.Control type="text" name="regex_valid" 
                        defaultValue={this.props.editData.regex_valid} 
                        placeholder="Regex_valid"/>
                    </Form.Group>
                    <Form.Group controlId="len_valid ">
                        <Form.Label>Len_valid</Form.Label>
                        <Form.Control type="number" name="len_valid" required
                        defaultValue={this.props.editData.len_valid}
                        placeholder="Len_valid"/>
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