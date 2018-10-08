import React from 'react';

import {Route, BrowserRouter} from 'react-router-dom';

import { hot } from 'react-hot-loader';

import LoginPage from './components/LoginPage';
import DashboardPage from './components/DashboardPage';
import NewUploadPage from './components/NewUploadPage';
import UploadManagerPage from './components/UploadManagerPage';


const App = () => {

    return (
        <BrowserRouter>
            <div>
                <Route exact path="/" component={ LoginPage }/>
                <Route exact path="/dashboard" component={ DashboardPage }/>
                <Route exact path="/upload_manager" component={ UploadManagerPage }/>
                <Route exact path="/upload_new" component={ NewUploadPage }/>
            </div>
        </BrowserRouter>
    );
};

// export default App;
export default hot(module)(App);
