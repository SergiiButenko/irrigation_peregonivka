import React from 'react';
import {Route, BrowserRouter} from 'react-router-dom';
import { hot } from 'react-hot-loader';
//import 'typeface-roboto';



import IrrigationPage from './IrrigationPage';


const App = () => {

    return (
        <BrowserRouter>
            <div>
                <Route exact path="/" component={ IrrigationPage }/>
                <Route exact path="/settings" component={ IrrigationPage }/>
                <Route exact path="/devices" component={ IrrigationPage }/>
            </div>
        </BrowserRouter>
    );
};

// export default App;
export default hot(module)(App);
