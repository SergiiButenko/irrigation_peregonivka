import React from 'react';
import {Route, BrowserRouter} from 'react-router-dom';
import { hot } from 'react-hot-loader';

import IrrigationPage from './IrrigationPage';
import ToolbarAppWeb from './ToolbarApp';
import 'typeface-roboto';

const App = () => {
    return (
        <BrowserRouter>
            <div>
                <Route exact path="/" component={ IrrigationPage }/>
                <Route exact path="/toolbar" component={ ToolbarAppWeb }/>
                <Route exact path="/devices" component={ IrrigationPage }/>
            </div>
        </BrowserRouter>
    );
};

export default hot(module)(App);
