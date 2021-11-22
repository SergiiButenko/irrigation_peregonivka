export const apiUri = {
    GROUPS: (groupId='') => 'api/v1/groups' + (groupId
    		? `/${groupId}`
			: ''),
	GROUPS_COMPONENTS: (groupId='') => `api/v1/groups/${groupId}/components`,	
    DEVICES: (deviceId='') => 'api/v1/devices' + (deviceId
    		? `/${deviceId}`
			: ''),
	COMPONENT_STATE: (componentId) => `api/v1/components/${componentId}/state`,
	COMPONENTS: (componentId) => `api/v1/components/${componentId}`,
    RULES: () => `api/v1/rules`,
    AUTH: () => 'api/v1/auth/login',
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
