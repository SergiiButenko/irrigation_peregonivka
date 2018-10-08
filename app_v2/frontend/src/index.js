import React from 'react';
import {Provider} from 'react-redux'
import ReactDOM from 'react-dom';

import store from './js/store'
import App from './App'

const title = 'My Minimal React Webpack Babel Setup';

import {MuiThemeProvider, createMuiTheme} from '@material-ui/core/styles';

const theme = createMuiTheme({
    palette: {
        primary: {
            main: '#a31919',
        },
        secondary: {
            main: 'rgb(55, 46, 142)',
        },
    },
});


ReactDOM.render(
	 <Provider store={store}>
        <MuiThemeProvider theme={theme}>
            <App/>
        </MuiThemeProvider>
     </Provider>,
document.getElementById('app')
);
