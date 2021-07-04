import React,{Component} from 'react';
import {Table} from 'react-bootstrap';

import {Button,ButtonToolbar} from 'react-bootstrap';
import {AddNewWorker} from './AddNewWorker.js';
import {EditWorker} from './EditWorker.js'
import { TestWorker } from './TestWorker.js';

export class WorkerSetup extends Component{

    constructor(props){
        super(props);
        this.state={workers:[], addModalShow:false, editModalShow:false, testWorker:{_show:false,_ID:"",_IP:""}}
    }

    refreshList(){
        fetch(process.env.REACT_APP_API +'worker/')
        .then(response=>response.json())
        .then(data=>{
            this.setState({workers:data});
        });
    }

    componentDidMount(){
        this.refreshList();
    }

    componentDidUpdate(){
        this.refreshList();
    }

    deleteWorker(worker_id){
        if(window.confirm('Are you sure?')){
            fetch(process.env.REACT_APP_API+'worker/',{
                method:'DELETE',
                header:{'Accept':'application/json',
            'Content-Type':'application/json'},
            body:JSON.stringify({
                id:worker_id      
            })})
        }
    }
    send_test_request(event, worker_id){
        event.preventDefault();
        fetch(process.env.REACT_APP_API +'test-worker/', {
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                id:worker_id      
            })
        })
        .then(response=>response.json())
        .then(
            data=>this.setState({testWorker:{
                _show:true,
                _IP:this.state.testWorker._IP,
                _name:this.state.testWorker._name,
                _response:data
            }})
        );

    }
    render(){
        const {workers, worker_id, worker_name, worker_ip, worker_rqmpass}=this.state;
        let addModalClose=()=>this.setState({addModalShow:false});
        let editModalClose=()=>this.setState({editModalShow:false});
        let testWorkerClose=()=>this.setState({testWorker:{_show:false,_name:"",_IP:"",_response:""}});
        return(
            <div className="container">
                <Table className="mt-4" striped bordered hover size="sm">
                    <thead>
                        <tr>
                        <th>Worker ID</th>
                        <th>Name</th>
                        <th>IP</th>
                        <th>Options</th>
                        </tr>
                    </thead>
                    <tbody>
                        {workers.map(worker=>
                            <tr key={worker.WorkerID}>
                                <td>{worker.WorkerID}</td>
                                <td>{worker.WorkerName}</td>
                                <td>{worker.WorkerIP}</td>
                                <td>
                                <ButtonToolbar>
                                    <Button className="mr-2" variant="info"
                                        onClick=
                                        {
                                            () => this.setState({
                                                editModalShow:true,
                                                worker_id: worker.WorkerID, 
                                                worker_name: worker.WorkerName,
                                                worker_ip: worker.WorkerIP, 
                                                worker_rqmpass: worker.RmqPassword
                                            })
                                        }
                                    >
                                        Edit
                                    </Button>

                                    <Button className="mr-2" variant="danger"
                                        onClick={()=>this.deleteWorker(worker.WorkerID)}>
                                        Delete
                                    </Button>
                                    <Button className="mr-2" variant="success"
                                        onClick={
                                            (event) => {
                                                this.setState({
                                                    testWorker:{
                                                        _show:true,
                                                        _IP:worker.WorkerIP,
                                                        _name:worker.WorkerName,
                                                        _response:"Waiting the worker for responding ..."
                                                }});
                                                this.send_test_request(event, worker.WorkerID)
                                            }
                                        }>
                                        Test
                                    </Button>
                                    
                                    <EditWorker 
                                        show={this.state.editModalShow}
                                        onHide={editModalClose}
                                        workerID={worker_id}
                                        workerName={worker_name}
                                        workerIP={worker_ip}
                                        workerRmqPass={worker_rqmpass}
                                    />

                                </ButtonToolbar>

                                </td>

                            </tr>)}
                    </tbody>

                </Table>
                <TestWorker
                    show={this.state.testWorker._show}
                    onHide={testWorkerClose}
                    workerIP={this.state.testWorker._IP}
                    workerName={this.state.testWorker._name}
                    response={this.state.testWorker._response}
                />
                <ButtonToolbar>
                    <Button 
                        variant='primary'
                        onClick={()=>this.setState({addModalShow:true})}
                    >
                        Add New Worker
                    </Button>

                    <AddNewWorker 
                        show={this.state.addModalShow}
                        onHide={addModalClose}
                    />
                </ButtonToolbar>
            </div>
        );
    }

}