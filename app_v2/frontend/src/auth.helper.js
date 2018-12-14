import {connectedRouterRedirect} from 'redux-auth-wrapper/history4/redirect';
import locationHelperBuilder from 'redux-auth-wrapper/history4/locationHelper';
import {ROLES} from './constants/roles';

const locationHelper = locationHelperBuilder({});

export const userIsAuthenticated = connectedRouterRedirect({
    redirectPath: '/login',
    authenticatedSelector: state => state.auth.user !== null,
    authenticatingSelector: state => !!state.auth.loggingIn,
    wrapperDisplayName: 'UserIsAuthenticated',
});


export const userIsNotAuthenticated = connectedRouterRedirect({
    redirectPath: (state, ownProps) => locationHelper.getRedirectQueryParam(ownProps) || '/',
    allowRedirectBack: false,
    authenticatedSelector: state => state.auth.user === null,
    authenticatingSelector: state => !!state.auth.loggingIn,
    wrapperDisplayName: 'UserIsNotAuthenticated',
});


export const userIsAdmin = connectedRouterRedirect({
    redirectPath: (state, ownProps) => locationHelper.getRedirectQueryParam(ownProps) || '/',
    allowRedirectBack: false,
    authenticatedSelector: state => state.auth.user !== null && isAdmin(state.auth.user),
    authenticatingSelector: state => !!state.auth.loggingIn,
    wrapperDisplayName: 'CheckIfUserIsAdmin',
});

export const isAdmin = (user) => {
    return hasRole(user, ROLES.admin)
};

export const hasRole = (user, roles) =>
    roles.some(role => user.roles.includes(role));

export const isAllowed = (user, rights) =>
    rights.some(right => user.rights.includes(right));
