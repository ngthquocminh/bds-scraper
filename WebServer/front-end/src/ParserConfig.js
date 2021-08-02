import React, { Component } from 'react';
import { Table, Dropdown }            from 'react-bootstrap';

import { Button, ButtonToolbar }    from 'react-bootstrap';
import { AddNewParser }             from './AddNewParser';
import { EditParser }               from './EditParser';


export class ParserConfig extends Component{

    constructor(props){
        super(props);
        this.state={parser_set:[], set_name:"", addModalShow:false, editModalShow:false, editModalData:{}}
    }

    refreshList(){
        fetch(process.env.REACT_APP_API +'parser/' + this.state.set_name + '/')
        .then(response=>response.json())
        .then(data=>{
            this.setState({parser_set:data});
        });
    }

    componentDidMount(){
        this.refreshList();
    }

    componentDidUpdate(){
        this.refreshList();
    }

    deleteParser(_id){
        if(window.confirm('Are you sure?')){
            fetch(process.env.REACT_APP_API+'parser/',{
                method:'DELETE',
                header:{'Accept':'application/json',
            'Content-Type':'application/json'},
            body:JSON.stringify({
                id:_id      
            })})
        }
    }

    render(){
        const {parser_set, set_name, editModalData}=this.state;
        let addModalClose=()=>this.setState({addModalShow:false});
        let editModalClose=()=>this.setState({editModalShow:false});
        return(
            <div className="ml-5 mr-5">
                <div className="row">
                    <div className="col">            
                        <Button 
                        variant="info"
                        onClick={(event)=>this.setState({set_name:"bat-dong-san-com-vn"})}
                        className="m-2"
                        >
                            batdongsan.com.vn
                        </Button>
                        <Button 
                        variant="info"
                        onClick={(event)=>this.setState({set_name:"nha-cho-tot-com"})}
                        className="m-2"
                        >
                            nha.chotot.com
                        </Button>
                        <Button 
                        variant="info"
                        onClick={(event)=>this.setState({set_name:"nha-dat-247-com-vn"})}
                        className="m-2"
                        >
                            nhadat247.com.vn
                        </Button>
                    </div>
                    <div className="col text-right">   
                        <Button 
                            variant='primary'
                            onClick={()=>this.setState({addModalShow:true})}
                        >
                            Add new attribute
                        </Button>

                    </div>
                </div>
                <hr/>
                <Table className="mt-4" striped bordered hover size="sm">
                    <thead>
                        <tr>
                        <th>Features</th>
                        <th>Default</th>
                        <th>Xpath</th>
                        <th>Pos_take</th>
                        <th>Regex_take</th>
                        <th>Regex_valid</th>
                        <th>Len_valid</th>
                        <th>Option</th>

                        </tr>
                    </thead>
                    <tbody>
                        {parser_set.map(parser=>
                            <tr key={parser.features}>
                                <td>{parser.features}</td>
                                <td>{parser.default}</td>
                                <td>{parser.xpath}</td>
                                <td>{parser.pos_take}</td>
                                <td>{parser.regex_take}</td>
                                <td>{parser.regex_valid}</td>
                                <td>{parser.len_valid}</td>

                                <td>
                                <ButtonToolbar>
                                    <Button className="mr-2" variant="info"
                                        onClick=
                                        {
                                            () => this.setState({
                                                editModalShow:true,
                                                editModalData:parser
                                            })
                                        }
                                    >
                                        Edit
                                    </Button>

                                    <Button className="mr-2" variant="danger"
                                        onClick={()=>this.deleteParser(parser.id)}>
                                        Delete
                                    </Button>
                                
                                </ButtonToolbar>

                                </td>

                            </tr>)}
                    </tbody>

                </Table>
                <EditParser 
                    show={this.state.editModalShow}
                    onHide={editModalClose}
                    editData={editModalData}
                />

                <AddNewParser 
                    show={this.state.addModalShow}
                    onHide={addModalClose}
                    setName={this.state.set_name}
                />
                 <hr/>
            </div>
        );
    }

}