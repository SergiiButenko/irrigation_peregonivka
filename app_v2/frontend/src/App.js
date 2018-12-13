import React from 'react';
import {Route, BrowserRouter} from 'react-router-dom';
import { hot } from 'react-hot-loader';
import 'typeface-roboto';

import {userIsAuthenticated, userIsNotAuthenticated} from './auth.helper';


import IrrigationPage from './components/IrrigationPage';
import CreateHubPage from './components/CreateHubPage';
import SignInPage from './components/SignInPage';
import DevicesPage from './components/DevicesPage';

const App = () => {
    return (
        <BrowserRouter>
            <div>
                <Route exact path="/" component={ userIsNotAuthenticated(IrrigationPage) }/>
                <Route exact path="/login" component={ userIsNotAuthenticated(SignInPage) }/>
                <Route exact path="/newhub" component={ userIsAuthenticated(CreateHubPage) }/>
                <Route exact path="/device" component={ userIsAuthenticated(DevicesPage) }/>
            </div>
        </BrowserRouter>
    );
};

export default hot(module)(App);
