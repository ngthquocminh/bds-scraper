import logo from './img/logo.svg';
import bg from './img/bg_789_1920.jpg'
import './Main.css';

import { HomePage }     from './HomePage';
import { WorkerSetup }  from './WorkersSetup';
import { ParserConfig } from './ParserConfig';
import { Navigation }   from './Navigation';
import { WorkerController } from './WorkerController';

import {BrowserRouter, Route, Switch} from 'react-router-dom';


function Main() {
  return (
    <BrowserRouter>
    <div className="p-5 text-center bg-image"  id="header-main" >
        <h1>WORKER CONTROLLER SYSTEM</h1>
        <Navigation/>

    </div>
    <div className="page-body">
        <Switch>
            <Route path='/' component={HomePage} exact/>
            <Route path='/worker-setup' component={WorkerSetup}/>
            <Route path='/parser-config' component={ParserConfig}/>
            <Route path='/worker-control' component={WorkerController}/>
            </Switch>
        </div>
    </BrowserRouter>

  );
}

export default Main;
