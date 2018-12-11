import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';
import PeopleIcon from '@material-ui/icons/People';
import BarChartIcon from '@material-ui/icons/BarChart';
import LayersIcon from '@material-ui/icons/Layers';
import AssignmentIcon from '@material-ui/icons/Assignment';
import DeviceHub from '@material-ui/icons/DeviceHub';
import DevicesOther from '@material-ui/icons/DevicesOther';
import Face from '@material-ui/icons/Face';


import {Link} from 'react-router-dom';

export const mainListItems = (
    <div>
        <ListItem component={Link} to="/" button>
            <ListItemIcon>
                <DashboardIcon />
            </ListItemIcon>
            <ListItemText primary="Полив" />
        </ListItem>

        <ListItem component={Link} to="/login"  button>
            <ListItemIcon>
                <Face />
            </ListItemIcon>
            <ListItemText primary="Login" />
        </ListItem>
    </div>
);

export const secondaryListItems = (
    <div>
        <ListSubheader inset>Адміністрування</ListSubheader>
        <ListItem component={Link} to="/newhub"  button>
            <ListItemIcon>
                <DeviceHub />
            </ListItemIcon>
            <ListItemText primary="Додати хаб" />
        </ListItem>

        <ListItem component={Link} to="/device"  button>
            <ListItemIcon>
                <DevicesOther />
            </ListItemIcon>
            <ListItemText primary="Пристрої" />
        </ListItem>
    </div>
);