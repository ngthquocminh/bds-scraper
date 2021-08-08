import React, { Component } from 'react';
import {Modal, Row, Col, Form} from 'react-bootstrap';
import { Button }    from 'react-bootstrap';
import BootstrapTable from 'react-bootstrap-table-next';
import filterFactory, { textFilter } from 'react-bootstrap-table2-filter';
import paginationFactory from 'react-bootstrap-table2-paginator';
import { PopUpParsedData } from './PopUpParsedData.js';


const columns = [{
    dataField: 'url',
    text: 'URL',
    filter: textFilter()
  }, {
    dataField: 'type',
    text: 'TYPE',
    filter: textFilter()
  }, {
    dataField: 'status',
    text: 'STATUS',
    filter: textFilter()
  },
  {
      dataField: 'date',
      text: 'DATE',
      filter: textFilter()
  },
  {
      dataField: 'url_hash',
      text: 'URL_HASH',
      filter: textFilter()
  },
  {
      dataField: 'post_date',
      text: 'POST_DATE',
      filter: textFilter()
  }
];

export class ParserTesting extends Component{

    constructor(props){
        super(props);
        this.handleSearchSubmit=this.handleSearchSubmit.bind(this);
        this.handleParseSubmit=this.handleParseSubmit.bind(this);

        this.state = {posts_data:[], popUpParsedData:[], popShow:false}
    }

    handleParseSubmit(event) {
        event.preventDefault();
        if (this.node.selectionContext.selected < 1)
            return;
        console.log(JSON.stringify({
            list_url_hash:this.node.selectionContext.selected,
            model_name_for_all:event.target.model.value
        }));
        fetch(process.env.REACT_APP_API+'test-parser/',{
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                list_url_hash:this.node.selectionContext.selected,
                model_name_for_all:event.target.model.value
            })
        })
        .then(res=>res.json())
        .then((result)=>{
            this.setState({popUpParsedData:result.content, popShow:true});
        },
        (error)=>{
            alert('Failed');
        })
    }


    handleSearchSubmit(event){
        event.preventDefault();
        fetch(process.env.REACT_APP_API+'load-post-html/',{
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                site:event.target.site.value,
                crawl_date: {
                    from:event.target.date_m_from.value + "/" + event.target.date_y_from.value,
                    to:event.target.date_m_to.value + "/" + event.target.date_y_to.value
                },
                post_date: {
                    from:event.target.post_date_m_from.value + "/" + event.target.post_date_y_from.value,
                    to:event.target.post_date_m_to.value + "/" + event.target.post_date_y_to.value
                },
                type: event.target.type.value,
                limit:event.target.limit.value
            })
        })
        .then(res=>res.json())
        .then((result)=>{
            console.log(result);
            this.setState({posts_data:result["content"]});
        },
        (error)=>{
            alert('Failed');
        })
    }
    
    render(){
        const { posts_data, popUpParsedData, popShow} = this.state
        console.log(popUpParsedData)
        let onHidePopUpData = () => {
            this.setState({popUpParsedData:[]});
            this.setState({popShow:false});
        }
        return(
            <div>
                <div className="ml-5 mr-5">
                    <Form onSubmit={this.handleSearchSubmit}>
                        <Row>   
                            <Col xs={2}>
                                <Form.Group controlId="site">
                                
                                <Form.Label>Site</Form.Label>
                                <Form.Control  defaultValue="" as="select" name="site">
                                    <option value="batdongsan.com.vn">batdongsan.com.vn</option>
                                    <option value="nha.chotot.com">nha.chotot.com</option>
                                    <option value="nhadat247.com.vn">nhadat247.com.vn</option>
                                </Form.Control>
                            </Form.Group>
                            </Col>
                            <Col xs={2} className="">
                                    <Col>
                                        <Form.Group controlId="crawl-date-from">                            
                                            <Form.Label>Crawl date from</Form.Label>
                                            <Row>
                                                <Col xs={3}>
                                                    <Form.Label>Month</Form.Label>
                                                </Col>
                                                <Col>
                                                    <Form.Control as="select" defaultValue="1" name="date_m_from">
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                        <option value="3">3</option>
                                                        <option value="4">4</option>
                                                        <option value="5">5</option>
                                                        <option value="6">6</option>
                                                        <option value="7">7</option>
                                                        <option value="8">8</option>
                                                        <option value="9">9</option>
                                                        <option value="10">10</option>
                                                        <option value="11">11</option>
                                                        <option value="12">12</option>

                                                    </Form.Control>
                                                </Col>                                    
                                            </Row>
                                            <Row>
                                                <Col xs={3}>
                                                    <Form.Label>Year</Form.Label>
                                                </Col>
                                                <Col>
                                                    <Form.Control as="select" defaultValue="2019" name="date_y_from">
                                                        <option value="2018">2018</option>
                                                        <option value="2019">2019</option>
                                                        <option value="2020">2020</option>
                                                        <option value="2021">2021</option>
                                                    </Form.Control>
                                                </Col>
                                            </Row>
                                        </Form.Group>
                                    </Col>
                                    <Col>
                                        <Form.Group controlId="crawl-date-to">                            
                                            <Form.Label>Crawl date to</Form.Label>
                                            <Row>
                                                <Col xs={3}>
                                                    <Form.Label>Month</Form.Label>
                                                </Col>
                                                <Col>
                                                    <Form.Control as="select" defaultValue="12" name="date_m_to">
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                        <option value="3">3</option>
                                                        <option value="4">4</option>
                                                        <option value="5">5</option>
                                                        <option value="6">6</option>
                                                        <option value="7">7</option>
                                                        <option value="8">8</option>
                                                        <option value="9">9</option>
                                                        <option value="10">10</option>
                                                        <option value="11">11</option>
                                                        <option value="12">12</option>
                                                    </Form.Control>
                                                </Col>                                    
                                            </Row>
                                            <Row>
                                                <Col xs={3}>
                                                    <Form.Label>Year</Form.Label>
                                                </Col>
                                                <Col>
                                                    <Form.Control  defaultValue="2021" as="select" name="date_y_to">
                                                        <option value="2018">2018</option>
                                                        <option value="2019">2019</option>
                                                        <option value="2020">2020</option>
                                                        <option value="2021">2021</option>
                                                    </Form.Control>
                                                </Col>
                                            </Row>
                                        </Form.Group>
                                    </Col>
                            </Col>                  
                            <Col xs={2} className="">
                                <Col>
                                    <Form.Group controlId="post-date-from">                            
                                        <Form.Label>Post date from</Form.Label>
                                        <Row>
                                            <Col xs={3}>
                                                <Form.Label>Month</Form.Label>
                                            </Col>
                                            <Col>
                                                <Form.Control defaultValue="1" as="select" name="post_date_m_from">
                                                    <option value="1">1</option>
                                                    <option value="2">2</option>
                                                    <option value="3">3</option>
                                                    <option value="4">4</option>
                                                    <option value="5">5</option>
                                                    <option value="6">6</option>
                                                    <option value="7">7</option>
                                                    <option value="8">8</option>
                                                    <option value="9">9</option>
                                                    <option value="10">10</option>
                                                    <option value="11">11</option>
                                                    <option value="12">12</option>
                                                </Form.Control>
                                            </Col>                                    
                                        </Row>
                                        <Row>
                                            <Col xs={3}>
                                                <Form.Label>Year</Form.Label>
                                            </Col>
                                            <Col>
                                                <Form.Control defaultValue="2020" as="select" name="post_date_y_from">
                                                    <option value="2018">2018</option>
                                                    <option value="2019">2019</option>
                                                    <option value="2020">2020</option>
                                                    <option value="2021">2021</option>
                                                </Form.Control>
                                            </Col>
                                        </Row>
                                    </Form.Group>
                                </Col>
                                <Col>
                                    <Form.Group controlId="post-date-from">                            
                                        <Form.Label>Post date to</Form.Label>
                                        <Row>
                                            <Col xs={3}>
                                                <Form.Label>Month</Form.Label>
                                            </Col>
                                            <Col>
                                                <Form.Control defaultValue="12" as="select" name="post_date_m_to">
                                                <option value="1">1</option>
                                                    <option value="2">2</option>
                                                    <option value="3">3</option>
                                                    <option value="4">4</option>
                                                    <option value="5">5</option>
                                                    <option value="6">6</option>
                                                    <option value="7">7</option>
                                                    <option value="8">8</option>
                                                    <option value="9">9</option>
                                                    <option value="10">10</option>
                                                    <option value="11">11</option>
                                                    <option value="12">12</option>
                                                </Form.Control>
                                            </Col>                                    
                                        </Row>
                                        <Row>
                                            <Col xs={3}>
                                                <Form.Label>Year</Form.Label>
                                            </Col>
                                            <Col>
                                                <Form.Control defaultValue="2021" as="select" name="post_date_y_to">
                                                    <option value="2018">2018</option>
                                                    <option value="2019">2019</option>
                                                    <option value="2020">2020</option>
                                                    <option value="2021">2021</option>
                                                </Form.Control>
                                            </Col>
                                        </Row>
                                    </Form.Group>
                                </Col>
                            </Col>
                            <Col xs={2}>
                                <Form.Group controlId="type">
                                    <Form.Label>Type</Form.Label>
                                    <Form.Control defaultValue="house" as="select" name="type">
                                        <option value="house">House</option>
                                        <option value="land">Land</option>
                                        <option value="apartment">Apartment</option>
                                    </Form.Control>
                                </Form.Group>
                            </Col>   
                            <Col xs={1}>
                                <Form.Group>
                                    <Form.Label>Status</Form.Label>
                                    <Form.Control type="number" name="status" defaultValue="0"
                                    placeholder="status"/>
                                </Form.Group>
                            </Col>
                            <Col xs={1}>
                                <Form.Group>
                                    <Form.Label>Limit</Form.Label>
                                    <Form.Control type="number" name="limit" defaultValue="20"
                                    placeholder="limit"/>
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Label className="text-white"> button </Form.Label>
                                <Form.Group>
                                    <Button variant="primary" type="submit">
                                        Search
                                    </Button>
                                </Form.Group>
                            </Col>
                        </Row>
                    </Form>
                </div>
                <hr/>
                <div className="ml-5 mr-5">
                    <Form onSubmit={this.handleParseSubmit}>
                        <Row>   
                            <Col xs={2}>
                                <Form.Label>Parser Model</Form.Label>
                                <Form.Group controlId="model">                                  
                                    <Form.Control as="select" defaultValue="auto" name="model">
                                        <option value="auto">auto</option>
                                        <option value="bat-dong-san-com-vn">bat-dong-san-com-vn</option>
                                        <option value="cho-tot-com">cho-tot-com</option>
                                        <option value="nha-dat-247-com-vn">nha-dat-247-com-vn</option> 
                                    </Form.Control>
                                </Form.Group>
                            </Col>
                            <Col xs={2}>
                                <Form.Label className="text-light">Submit</Form.Label>
                                <Form.Group controlId="parse-submit">                                    
                                    <Button className="btn btn-default"  type="submit"> Parse Selected Posts </Button>
                                </Form.Group>
                            </Col>
                        </Row>
                    </Form>
                    <BootstrapTable
                        ref={ n => this.node = n }
                        keyField="url_hash"
                        data={ posts_data }
                        columns={ columns }
                        filter={ filterFactory() }
                        pagination={ paginationFactory() }
                        selectRow={ { mode: 'checkbox', clickToSelect: true } }
                    />
                    <PopUpParsedData show={popShow} onHide={onHidePopUpData} json_data={popUpParsedData}/>
                </div>
            </div>
        );
    }

}