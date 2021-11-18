export const apiUri = {
    GROUPS: (groupId='') => 'api/v1/groups' + (groupId
    		? `/${groupId}`
			: ''),
	GROUPS_COMPONENTS: (groupId='') => `api/v1/groups/${groupId}/components`,	
    DEVICES: (deviceId='') => 'api/v1/devices' + (deviceId
    		? `/${deviceId}`
	    	: ''),
    RULES: () => `api/v1/rules`,
    AUTH: () => 'api/v1/auth/login',
    AUTH_REFRESH: () => 'api/v1/auth/refreshToken',
	LOGOUT: () => 'api/v1/auth/logout',
	USER: () => 'api/v1/auth/me',
	WEATHER_FORECAST: () => 'api/v1/dashboard/weather/forecast',
	IRRIGATION_FORECAST: () => 'api/v1/dashboard/rules/irrigation/forecast',
};

export const webUri = {
	GROUPS: (groupId='') => '/groups' + (groupId
		? `/${groupId}`
		: ''),
	DEVICES: (deviceId='') => '/devices' + (deviceId
		? `/${deviceId}`
		: ''),
};
