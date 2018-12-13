import {connectedRouterRedirect} from 'redux-auth-wrapper/history4/redirect';
import locationHelperBuilder from 'redux-auth-wrapper/history4/locationHelper';
//import LoggingInPage from './components/LoggingInPage';

const locationHelper = locationHelperBuilder({});

export const userIsAuthenticated = connectedRouterRedirect({
    redirectPath: '/login',
    authenticatedSelector: state => state.auth.user !== null,
    authenticatingSelector: state => !!state.auth.loggingIn,
    // AuthenticatingComponent: LoggingInPage,
    wrapperDisplayName: 'UserIsAuthenticated',
});


export const userIsNotAuthenticated = connectedRouterRedirect({
    redirectPath: (state, ownProps) => locationHelper.getRedirectQueryParam(ownProps) || '/',
    allowRedirectBack: false,
    authenticatedSelector: state => state.auth.user === null,
    authenticatingSelector: state => !!state.auth.loggingIn,
    // AuthenticatingComponent: LoggingInPage,
    wrapperDisplayName: 'UserIsNotAuthenticated',
});
