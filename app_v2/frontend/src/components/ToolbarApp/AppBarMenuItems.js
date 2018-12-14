import React from 'react';

import Divider from '@material-ui/core/Divider/Divider';
import CommonMenu from './CommonMenu';
import AdminMenu from './AdminMenu';

export const AppBarMenuItems = (
    <>
        <Divider/>
        <CommonMenu />
        <Divider/>
        <AdminMenu/>
    </>
);

export default AppBarMenuItems;