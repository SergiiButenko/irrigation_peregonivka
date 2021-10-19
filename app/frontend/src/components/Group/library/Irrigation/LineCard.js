import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import Battery20 from '@material-ui/icons/Battery20';
import Battery60 from '@material-ui/icons/Battery60';
import Battery90 from '@material-ui/icons/Battery90';
import connect from 'react-redux/es/connect/connect';
import { toggleSelection } from '../../../../actions/groups';
import { getGroups } from '../../../../selectors/groups';
import { withRouter } from 'react-router-dom';
import classNames from 'classnames';


const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
    selected: {
        boxShadow: '0 0 0 3px #8dbdf7',
        background: '#dae7f7',
    },
});
const mapStateToProps = (state) => {
    return getGroups(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, { toggleSelection })
export default class LineCard extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        groups: PropTypes.object.isRequired,
        acuatorId: PropTypes.string.isRequired,
        groupId: PropTypes.string.isRequired,
    };

    render() {
        const {acuatorId, groupId, groups, classes, toggleSelection} = this.props;
        const actuator = groups[groupId].components[acuatorId];
        
        actuator.selected = !!actuator.selected || false;
        return (
            <Paper
                className={classNames(classes.root, actuator.selected && classes.selected)}
                elevation={1}
                onClick={() => toggleSelection(groupId, acuatorId)}
            >
                <Grid
                    container
                    spacing={24}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <Grid item xs={6}>
                        <Typography variant="h5" component="h3">
                            {actuator.name}
                        </Typography>
                        <Typography component="p">
                            {actuator.description + " " + actuator.selected}
                        </Typography>
                        <Typography component="p">
                            {JSON.stringify(actuator.settings, null, 2)}
                        </Typography>
                    </Grid>
                    <Grid item>
                        <Battery20 />
                        <Battery60 />
                        <Battery90 />
                    </Grid>
                </Grid>
            </Paper>
        );
    }
}
