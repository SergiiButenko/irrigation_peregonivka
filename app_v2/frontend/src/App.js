import React from 'react';
import {Route, BrowserRouter} from 'react-router-dom';
import { hot } from 'react-hot-loader';
import 'typeface-roboto';

import IrrigationPage from './IrrigationPage';
import CreateHubPage from './CreateHubPage';
import SignInPage from './SignInPage';
import DevicesPage from './DevicesPage';

const App = () => {
    return (
        <BrowserRouter>
            <div>
                <Route exact path="/" component={ IrrigationPage }/>
                <Route exact path="/login" component={ SignInPage }/>
                <Route exact path="/newhub" component={ CreateHubPage }/>
                <Route exact path="/device" component={ DevicesPage }/>
            </div>
        </BrowserRouter>
    );
};

export default hot(module)(App);
