import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Slider from '@material-ui/lab/Slider';
import Collapse from '@material-ui/core/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import AccessTime from '@material-ui/icons/AccessTime';
import Button from '@material-ui/core/Button';
import PageSpinner from '../../shared/PageSpinner';
import LoadingFailed from '../../shared/LoadingFailed';

import connect from 'react-redux/es/connect/connect';
import {
    changeSettings
} from '../../../actions/groups';

import { initComponent, setComponentState } from '../../../actions/device'
import { getDevices } from '../../../selectors/devices';
import { withRouter } from 'react-router-dom';
import classNames from 'classnames';
import { getGroups } from '../../../selectors/groups';


const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
    card: {
        minWidth: 275,
        marginBottom: theme.spacing.unit,
    },
    cardOn: {
        boxShadow: '0 0 0 3px #008e21',
    },
    expandMore: {
        transform: 'rotate(360deg)',
        transition: '300ms transform',
    },
    expandMore_selected: {
        transform: 'rotate(180deg)',
        transition: '300ms transform',
    },
    slider: {
        padding: '16px 0px',
        marginRight: theme.spacing.unit * 2,
    },
});


const mapStateToProps = (state) => {
    return {'groups': getGroups(state),
            'devices': getDevices(state)};
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, { changeSettings, initComponent, setComponentState })
export default class Switcher extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        groups: PropTypes.object.isRequired,
        devices: PropTypes.object.isRequired,
        componentId: PropTypes.string.isRequired,
        groupId: PropTypes.string.isRequired,
    };

    componentDidMount() {
        this.props.initComponent(this.props.componentId)
    }

    getMinutes = () => {
        const actuator = this.props.groups.groups[this.props.groupId].components[this.props.componentId];
        return actuator.settings.minutes;
    };
    
    calculate_min = () => {
        const minutes = this.getMinutes();
        return Math.round(minutes * 0.25);
    };

    calculate_max = () => {
        const minutes = this.getMinutes();
        return minutes * 2;

    };

    calculate_step = () => {
        const minutes = this.getMinutes();
        if (minutes >= 60) {
            return 60;
        }

        return 5;
    };

    state = {
        collapsed: false,
        min_minutes: this.calculate_min(),
        max_minutes: this.calculate_max(),
        step_minutes: this.calculate_step(),
    };

    handleCollapse = () => {
        this.setState(state => ({ collapsed: !state.collapsed }));
    };

    handleChangeMinutes = (event, value_minutes) => {
        this.props.changeSettings(
            this.props.groupId,
            this.props.componentId,
            'minutes',
            value_minutes
            );
    };

    render() {
        const { componentId, groupId, groups: { groups }, classes, setComponentState, 
                devices: { devices, loading, deviceFetchError}  } = this.props;
        const { collapsed, min_minutes, max_minutes, step_minutes } = this.state;

        if (loading) {
            return <PageSpinner />;
        }

        if (deviceFetchError) {
            return <LoadingFailed errorText={deviceFetchError} />;
        }
        
        const actuator = groups[groupId].components[componentId];
        const isON = devices.components[componentId].state == 1;
        
        const minutes = actuator.settings.minutes;
        return (
            <Card className={classNames(classes.card, isON && classes.cardOn)}>
                <CardContent className={classes.content}>
                    <Grid item
                        container
                        direction="row"
                        spacing={16}
                        >
                        <Grid item>
                            <Typography gutterBottom variant="h5" component="h2">
                                {actuator.name}
                            </Typography>
                        </Grid>
                    </Grid>
                    <Grid item container direction="row" spacing={16} onClick={this.handleCollapse} justify="flex-end">
                        <Grid item>
                            <Typography component="p">Включити на {minutes} хв</Typography>
                        </Grid>
                        <Grid item xs>
                            <ExpandMoreIcon
                                className={collapsed ? classes.expandMore_selected : classes.expandMore} />
                        </Grid>
                    </Grid>
                    <Collapse in={collapsed}>
                        <Grid item container direction="row" spacing={16} justify="center"
                            alignItems="center">
                            <Grid item xs>
                                <AccessTime />
                            </Grid>
                            <Grid item xs={10}>
                                <Slider
                                    classes={{ container: classes.slider }}
                                    value={minutes}
                                    min={min_minutes}
                                    max={max_minutes}
                                    step={step_minutes}
                                    onChange={this.handleChangeMinutes}
                                />
                            </Grid>
                        </Grid>
                    </Collapse>
                </CardContent>

                <CardActions
                >
                    <Button
                        color="primary"
                        className={classes.button}
                        onClick={() => setComponentState(componentId, !isON)}
                    >
                        {isON ? 'Виключити' : 'Включити'}
                    </Button>
                </CardActions>
            </Card>
        );
    }
}