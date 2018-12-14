import React, {Component} from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

import {Link} from 'react-router-dom';
import List from '@material-ui/core/List/List';
import {isAdmin} from '../../helpers/auth.helper';
import ListSubheader from '@material-ui/core/ListSubheader/ListSubheader';
import DeviceHub from '@material-ui/core/SvgIcon/SvgIcon';

export default class AdminMenu extends Component {
    render() {
        const {user} = this.props;

        if (isAdmin(user)) {
            return null;
        }

        return (
            <List>
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
            </List>
        );
    }
}