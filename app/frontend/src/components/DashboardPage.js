import React from 'react';
import Dashboard from './Dashboard/index';
import ToolbarAppWeb from './ToolbarApp';


const DashboardPage = () => (
    <div>
        <ToolbarAppWeb>
            <Dashboard/>
        </ToolbarAppWeb>
    </div>
);

export default DashboardPage;