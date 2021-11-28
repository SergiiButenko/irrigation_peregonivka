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

import { initComponent, createIntervals, deleteInterval } from '../../../actions/device';
import { getDevices } from '../../../selectors/devices';
import { withRouter } from 'react-router-dom';
import classNames from 'classnames';


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
    return getDevices(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, { initComponent, createIntervals, deleteInterval })
export default class Switcher extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        devices: PropTypes.object.isRequired,
        componentId: PropTypes.string.isRequired,
    };

    getMinutes = () => {
        const actuator = this.props.devices.components[this.props.componentId];
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
        min_minutes: null,
        max_minutes: null,
        step_minutes: null,
        component: null,
        value_minutes: null
    };

    componentDidMount() {
        this.props.initComponent(this.props.componentId);
    };

    componentWillReceiveProps(nextProps) {
        if (this.props !== nextProps && nextProps.loading == false) {
            this.setState({ min_minutes: this.calculate_min() });
            this.setState({ max_minutes: this.calculate_max() });
            this.setState({ step_minutes: this.calculate_step() });
            this.setState({ component: this.props.devices.components[this.props.componentId] });
            this.setState(state => ({ value_minutes: state.component.settings.minutes }));
        }
    }

    handleCollapse = () => {
        this.setState(state => ({ collapsed: !state.collapsed }));
    };

    handleChangeMinutes = (event, value_minutes) => {
        this.setState({ value_minutes });
    };

    toggleComponentState = () => {
        const interval = this.state.component.state.interval;
        
        if (interval == null) {
            return this.props.createIntervals(this.state.component, this.state.value_minutes);
        }
        
        this.props.deleteInterval(
            this.state.component.id,
            interval.id,
            this.state.component.default_state
            )
    };

    render() {
        const { classes, loading, deviceFetchError } = this.props;
        const { collapsed, min_minutes, max_minutes, step_minutes, value_minutes, component } = this.state;

        if (loading) {
            return <PageSpinner />;
        }

        if (deviceFetchError) {
            return <LoadingFailed errorText={deviceFetchError} />;
        }

        const isON = component.state.expected_state == 1;

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
                                {component.name}
                            </Typography>
                        </Grid>
                    </Grid>
                    <Grid item container direction="row" spacing={16} onClick={this.handleCollapse} justify="flex-end">
                        <Grid item>
                            <Typography component="p">Включити на {value_minutes} хв</Typography>
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
                                    value={value_minutes}
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
                        onClick={this.toggleComponentState}
                    >
                        {isON ? 'Виключити' : 'Включити'}
                    </Button>
                </CardActions>
            </Card>
        );
    }
}