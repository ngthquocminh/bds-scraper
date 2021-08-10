import React, { Component } from 'react';
import { Row, Col, Form } from 'react-bootstrap';
import { Table } from 'react-bootstrap';
import { Button, ButtonToolbar } from 'react-bootstrap';


export class ParseController extends Component {

    constructor(props) {
        super(props);
        this.handleDoCrawlSubmit = this.handleDoCrawlSubmit.bind(this);
        this.handleCrawlDateEnable = this.handleCrawlDateEnable.bind(this);
        this.handlePostDateEnable = this.handlePostDateEnable.bind(this);
        this.state = { workers: [] , crawlDateEnable:true, postDateEnable:true };
    }
    refreshList() {
        fetch(process.env.REACT_APP_API + 'worker-info/', { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                this.setState({ workers: data });
            });
    }

    componentDidMount() {
        this.refreshList();
    }

    componentDidUpdate() {
        this.refreshList();
    }

    handleCrawlDateEnable(event) {
        this.setState({crawlDateEnable:!this.state.crawlDateEnable});
    }

    handlePostDateEnable(event) {
        this.setState({postDateEnable:!this.state.postDateEnable});
    }

    handleDoCrawlSubmit(event) {
        event.preventDefault();
        fetch(process.env.REACT_APP_API + 'do-parse/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                site: event.target.site.value,
                crawl_date: this.state.crawlDateEnable ? {
                    from: event.target.date_m_from.value + "/" + event.target.date_y_from.value,
                    to: event.target.date_m_to.value + "/" + event.target.date_y_to.value
                } : null,
                post_date: this.state.postDateEnable? {
                    from: event.target.post_date_m_from.value + "/" + event.target.post_date_y_from.value,
                    to: event.target.post_date_m_to.value + "/" + event.target.post_date_y_to.value
                } : null,
                type: event.target.type.value,
                model: event.target.model.value,
                status: event.target.status.value,
                num_workers: event.target.num_workers.value,
                limit: event.target.limit.value
            })
        })
        .then(res => res.json())
        .then((result) => {
            console.log(result);
        },
        (error) => {
            alert('Failed');
        })
    }
    pauseWorker(id) {
        fetch(process.env.REACT_APP_API + 'pause-worker/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id
            })
        })
        .then(res => res.json())
        .then((result) => {
            console.log(result);
        },
        (error) => {
            alert('Failed');
        })
    }
    stopWorker(id) {
        fetch(process.env.REACT_APP_API + 'stop-worker/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: id
            })
        })
        .then(res => res.json())
        .then((result) => {
            console.log(result);
        },
        (error) => {
            alert('Failed');
        })
    }
    stopAllWorker() {
        fetch(process.env.REACT_APP_API + 'stop-all-worker/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then((result) => {
            console.log(result);
        },
        (error) => {
            alert('Failed');
        })
    }
    render() {
        const { workers, crawlDateEnable, postDateEnable } = this.state;
        return (
            <div>
                <div className="ml-5 mr-5">
                    <Form onSubmit={this.handleDoCrawlSubmit}>
                        <Row>
                            <Col xs={2}>
                                <Form.Group controlId="site">
                                    <Form.Label>Site</Form.Label>
                                    <Form.Control defaultValue="batdongsan.com.vn" as="select" name="site">
                                        <option value="batdongsan.com.vn">batdongsan.com.vn</option>
                                        <option value="chotot.com">nha.chotot.com</option>
                                        <option value="nhadat247.com.vn">nhadat247.com.vn</option>
                                    </Form.Control>
                                </Form.Group>
                            </Col>

                            <Col xs={2} className="">
                                <Form.Group controlId="crawl-date-enable">
                                    <Form.Check checked={crawlDateEnable} name="crawl_date_enable" type="checkbox" onChange={this.handleCrawlDateEnable}  label="Crawl date range" />
                                </Form.Group>
                                { crawlDateEnable ?
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
                                                <Form.Control defaultValue="2021" as="select" name="date_y_to">
                                                    <option value="2018">2018</option>
                                                    <option value="2019">2019</option>
                                                    <option value="2020">2020</option>
                                                    <option value="2021">2021</option>
                                                </Form.Control>
                                            </Col>
                                        </Row>
                                    </Form.Group>
                                </Col>
                                :<div></div>
                                }
                            </Col>
                            <Col xs={2} className="">
                                <Form.Group controlId="post-date-enable">
                                    <Form.Check checked={postDateEnable} name="post_date_enable" type="checkbox" onChange={this.handlePostDateEnable}  label="Post date range" />
                                </Form.Group>
                                { postDateEnable? 
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
                                    <Form.Group controlId="post-date-to">
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
                                : <div></div>
                                }
                            </Col>
                            <Col xs={1}>
                                <Form.Group controlId="type">
                                    <Form.Label>Type</Form.Label>
                                    <Form.Control defaultValue="house" as="select" name="type">
                                        <option value="all">All</option>
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
                            <Col xs={2}>
                                <Form.Label>Parser Model</Form.Label>
                                <Form.Group controlId="model">                                  
                                    <Form.Control as="select" defaultValue="auto" name="model">
                                        <option value="bat-dong-san-com-vn">bat-dong-san-com-vn</option>
                                        <option value="nha-cho-tot-com">cho-tot-com</option>
                                        <option value="nha-dat-247-com-vn">nha-dat-247-com-vn</option> 
                                        {/* <option value="spacy-parser">spacy-parser</option> */}
                                    </Form.Control>
                                </Form.Group>
                            </Col>
                            <Col xs={1}>
                                <Form.Group>
                                    <Form.Label>Limit of posts</Form.Label>
                                    <Form.Control type="number" name="limit" defaultValue="20000"
                                        placeholder="limit" />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row className="text-right">
                            <Col></Col>
                            <Col xs={2}>
                                <Form.Group>
                                    <Form.Label>Number of workers</Form.Label>
                                    <Form.Control type="number" name="num_workers" defaultValue="3"
                                    placeholder="num of workers"/>
                                </Form.Group>
                            </Col>
                            <Col xs={2}>
                                <Form.Label className="text-white"> button </Form.Label>
                                <Form.Group>
                                    <Button variant="primary" type="submit">
                                        Start Parsing
                                    </Button>
                                </Form.Group>
                            </Col>
                        </Row>
                    </Form>
                </div>
                <hr />
                <div className="container">
                    <div className="text-right">
                        <Button className="mr-2" variant="danger"
                            onClick={() => this.stopAllWorker()}>
                            Stop All
                        </Button>
                    </div>
                    <div className="">
                        <Table className="mt-4" striped bordered hover size="sm">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Status</th>
                                    <th>Info</th>
                                    <th>Options</th>
                                </tr>
                            </thead>
                            <tbody>
                                {workers.map(worker =>
                                    <tr key={worker.id}>
                                        <td>{worker.name}</td>
                                        <td>{worker.status}</td>
                                        <td>{worker.info}</td>
                                        <td>
                                            <ButtonToolbar>
                                                <Button className="mr-2" variant="info"
                                                    onClick={() => this.pauseWorker(worker.id)}
                                                >
                                                    {
                                                    worker.status.includes("pause")
                                                    ?<i class="fas fa-play"></i>
                                                    :<i class="fas fa-pause"></i>
                                                    }          
                                                </Button>

                                                <Button className="mr-2" variant="danger"
                                                    onClick={() => this.stopWorker(worker.id)}>
                                                    <i class="fas fa-stop"></i>
                                                </Button>          

                                            </ButtonToolbar>

                                        </td>

                                    </tr>)}
                            </tbody>

                        </Table>
                    </div>
                </div>
            </div>
        );
    }

}