import React,{Component} from 'react';
import {NavLink} from 'react-router-dom';
import {Navbar,Nav} from 'react-bootstrap';

export class Navigation extends Component{

    render(){
        return(
            <Navbar expand="lg">
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav>
                <NavLink className="d-inline p-2 ml-3 bg-dark text-white" to="/">
                    Home
                </NavLink>
                <NavLink className="d-inline p-2 ml-3 bg-dark text-white" to="/worker-setup">
                    Worker Setup
                </NavLink>
                <NavLink className="d-inline p-2 ml-3 bg-dark text-white" to="/parser-config">
                    Parser Config
                </NavLink>
                <NavLink className="d-inline p-2 ml-3 bg-dark text-white" to="/parser-testing">
                    Parser Testing
                </NavLink>
                <NavLink className="d-inline p-2 ml-3 bg-dark text-white" to="/crawl-control">
                    Crawl Controller
                </NavLink>
                <NavLink className="d-inline p-2 ml-3 bg-dark text-white" to="/parse-control">
                    Parse Controller
                </NavLink>
                </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}