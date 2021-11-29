import providerBase from './base';
import {withAuth, tokenRefresh} from './middlewares';

import {apiUri} from '../constants/uri';
import {parseJwt} from '../helpers/auth.helper';
import {adminOnly} from './helpers';

class SmartSystemApi {
    config = {};

    constructor(config = {}) {
        this.provider = providerBase;
        this.setGlobalConfig(config);

        this.user = {};
    }

    setGlobalConfig(config) {
        this.config = config;
        this.provider.setGlobalConfig(config);
    }

    async login(username, password, options = {}) {
        // Build formData object.
        let formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const data = new URLSearchParams(formData);
        options.headers = {...options.headers, 'Content-Type': 'application/x-www-form-urlencoded'}
        
        const {access_token, refresh_token} = await this.provider.post(
            apiUri.AUTH(),
            data,
            options,
        );

        let jwt = parseJwt(access_token);

        const user = {
            name: jwt.sub,
            accessToken: access_token,
            refreshToken: refresh_token,
            roles: jwt.user_claims.roles
        };

        smartSystemApi.setUserData(user);

        return this;
    }

    async setUserByAccessToken(accessToken, options = {}) {
       
        await this.provider.get(
            apiUri.USER(),
            {headers: {'Authorization': `Bearer ${accessToken}`}},
        );

        let jwt = parseJwt(accessToken);

        const user = {
            name: jwt.sub,
            accessToken: accessToken,
            refreshToken: accessToken,
            roles: jwt.user_claims.roles
        };

        smartSystemApi.setUserData(user);

        return this;
    }

    async logout(options = {}) {
        await this.provider.delete(
            apiUri.LOGOUT(),
            options,
        );

        return this;
    }

    setUserData({name, accessToken, refreshToken, roles}) {
        this.user = {name, accessToken, refreshToken, roles};

        this.provider.setMiddlewares([
            tokenRefresh, // removed handler from tokenRefresh fucntion
            withAuth(),
        ]);
    }

    async getDevice(options = {}) {
        return this.provider.get(
            apiUri.DEVICES(),
            options,
        );
    }

    async getDeviceById(deviceId, options = {}) {
        return this.provider.get(
            apiUri.DEVICES(deviceId),
            options,
        );
    }

    async getDeviceComponentState(componentId, options = {}) {
        return this.provider.get(
            apiUri.COMPONENT_STATE(componentId),
            options,
        );
    }

    async setDeviceComponentState(componentId, options = {}) {
        return this.provider.put(
            apiUri.COMPONENT_STATE(componentId),
            options,
        );
    }

    async getDeviceComponent(componentId, options = {}) {
        return this.provider.get(
            apiUri.COMPONENTS(componentId),
            options,
        );
    }


    async createIntervals(body, options = {}) {
        options.headers = {
            ...options.headers, "Content-Type": "application/json; charset=utf-8"
        };
        
        return this.provider.post(
            apiUri.INTERVALS(),
            JSON.stringify(body),
            options,
        );
    };

    async deleteInterval(intervalId, body, options = {}) {
        options.headers = {
            ...options.headers, "Content-Type": "application/json; charset=utf-8"
        };

        return this.provider.delete(
            apiUri.INTERVALS(intervalId),
            JSON.stringify(body),
            options,
        );
    };


    async getGroup(groupId, options = {}) {
        return this.provider.get(
            apiUri.GROUPS(groupId),
            options,
        );
    }

    async getGroupComponentsById(groupId, options = {}) {
        return this.provider.get(
            apiUri.GROUPS_COMPONENTS(groupId),
            options,
        );
    }

    async getDashboard() {
        let data = {
            'irrigation_forecast': null,
            'weather_forecast': null
        };

        data.weather_forecast = await this.provider.get(
            apiUri.WEATHER_FORECAST()
        );

        data.irrigation_forecast = await this.provider.get(
            apiUri.IRRIGATION_FORECAST()
        );

        return data;
    }
}

export const smartSystemApi = new SmartSystemApi();
