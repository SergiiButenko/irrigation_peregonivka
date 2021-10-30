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
};

export const webUri = {
	GROUPS: (groupId='') => '/groups' + (groupId
		? `/${groupId}`
		: ''),
	DEVICES: (deviceId='') => '/devices' + (deviceId
		? `/${deviceId}`
		: ''),
};
