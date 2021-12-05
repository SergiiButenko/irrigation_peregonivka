import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import PageSpinner from '../../components/shared/PageSpinner';
import LoadingFailed from '../../components/shared/LoadingFailed';

import connect from 'react-redux/es/connect/connect';

import { initSensor } from '../../actions/device';
import { getDevices } from '../../selectors/devices';
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
    errorMessage: {
        color: 'red',
    }
});


const mapStateToProps = (state) => {
    return getDevices(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, { initSensor })
export default class PowerCurrentV1 extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        devices: PropTypes.object.isRequired,
        componentId: PropTypes.string.isRequired,
    };


    state = {
        component: null,
        loading: true
    };

    componentDidMount() {
        this.props.initSensor(this.props.componentId);
    };

    componentWillReceiveProps(nextProps) {
        if (this.props !== nextProps
            && nextProps.loading == false
            && nextProps.devices.components
            && nextProps.devices.components[this.props.componentId] != undefined
        ) {
            this.setState({ loading: false });
            this.setState({ component: nextProps.devices.components[this.props.componentId] });
            console.log(nextProps)
        }
    }

    validateData = (data) => {
        let res = { exist: false, expired: false };
        if (data.length == 0) {
            res.exist = false;
            res.expired = false;
            return res;
        } else {
            res.exist = true;
        }

        const difference = data[0].date - new Date();
        if (Math.floor((difference/1000)/60) > -60) {
            res.expired = true;
        } else {
            res.expired = false;
        }

        return res
    };

    render() {
        const { classes, deviceFetchError } = this.props;
        const { loading, component } = this.state;

        if (loading) {
            return <PageSpinner />;
        }

        if (deviceFetchError) {
            return <LoadingFailed errorText={deviceFetchError} />;
        }


        const data = component.data;
        const isDataValid = this.validateData(data);
        
        let message = { 'text': '', classes: null };
        
        if (isDataValid.exist == true) {
            const levelHigh = data[0].data.level == 1;
            message.text = (levelHigh ? 'Рівень сигналу високий' : 'Рівень сигналу низький');
        } else if (isDataValid.exist == false) {
            message.text = "Немає жодних даних. Перевірте сенсор";
            message.classes = classes.errorMessage;
        } else if (isDataValid.expired == true) {
            message = "Дані сенсора застаріли. Перевірте сенсор";
            message.classes = classes.errorMessage;
        }

        return (
            <Card className={classes.card}>
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
                    <Grid item container direction="row" spacing={16} justify="flex-start">
                        <Grid item>
                            <Typography component="p" className={message.classes}>
                                {message.text}
                            </Typography>
                        </Grid>
                    </Grid>
                </CardContent>

                <CardActions
                >
                    <Button
                        color="primary"
                        className={classes.button}
                    // onClick={this.toggleComponentState}
                    // disabled={updating}
                    >
                        Показати деталі
                    </Button>
                </CardActions>
            </Card>
        );
    }
}