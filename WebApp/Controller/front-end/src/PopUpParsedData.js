import React,{Component, WebView} from 'react';
import {Modal,Button, Row, Col, Form} from 'react-bootstrap';
import ReactJson from 'react-json-view'
import "./JsonView.css";

const json_lib = {
    replacer: function(match, pIndent, pKey, pVal, pEnd) {
       var key = '<span class=json-key>';
       var val = '<span class=json-value>';
       var str = '<span class=json-string>';
       var r = pIndent || '';
       if (pKey)
          r = r + key + pKey.replace(/[": ]/g, '') + '</span>: ';
       if (pVal)
          r = r + (pVal[0] == '"' ? str : val) + pVal + '</span>';
       return r + (pEnd || '');
    },
    prettyPrint: function(obj) {
       var jsonLine = /^( *)("[\w]+": )?("[^"]*"|[\w.+-]*)?([,[{])?$/mg;
       return JSON.stringify(obj, null, 3)
          .replace(/&/g, '&amp;').replace(/\\"/g, '&quot;')
          .replace(/</g, '&lt;').replace(/>/g, '&gt;')
          .replace(jsonLine, json_lib.replacer);
    }
};
    

export class PopUpParsedData extends Component{
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
                    <Modal.Header>
                        <Modal.Title id="contained-modal-title-vcenter">
                            Parser Test Result
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Row>
                            <Col xs={9}>
                            <ReactJson src={this.props.json_data} />
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