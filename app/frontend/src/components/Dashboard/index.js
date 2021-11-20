import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';

import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';

import { getDashboard } from '../../selectors/dashboard';
import { fetchDashboard } from '../../actions/dashboard';
import PageSpinner from '../shared/PageSpinner';
import LoadingFailed from '../shared/LoadingFailed';

import { Typography } from '@material-ui/core';
import { formIrrigationData, formWeatherData } from '../../helpers/dahsboard.helpers';

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
    table: {
        minWidth: 700,
    },
});

const mapStateToProps = (state) => {
    return getDashboard(state);
};
@withStyles(styles)
@connect(mapStateToProps, { fetchDashboard })
export default class Dashboard extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        data: PropTypes.array.isRequired,
        dashboardFetchError: PropTypes.any,
    };

    componentDidMount() {
        this.props.fetchDashboard();
    }

    render() {
        const { classes, loading, dashboardFetchError, data } = this.props;

        if (loading) {
            return <PageSpinner />;
        }

        if (dashboardFetchError) {
            return <LoadingFailed errorText={dashboardFetchError} />;
        }

        console.log(data);
        const weatherData = formWeatherData(data.weather_forecast.hourly);
        const irrigationData = formIrrigationData(data.irrigation_forecast);

        return (
            <>
                <Grid
                    container
                    spacing={24}
                    direction="column"
                    // justify="space-between"
                    alignItems="center"
                >
                    <Grid item>
                        <Typography gutterBottom variant="h5" component="h2">
                            Полив
                            </Typography>
                        <Paper className={classes.root}>
                            <Table className={classes.table}>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Ділянка поливу</TableCell>
                                        <TableCell align="right">Час початку</TableCell>
                                        <TableCell align="right">Дія</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {irrigationData.length == 0
                                        ? <TableCell component="th" scope="row" align="center">
                                            Немає запланованого поливу
                                        </TableCell>
                                        : irrigationData.map(row => (
                                            <TableRow key={row.name}>
                                                <TableCell component="th" scope="row">
                                                    {row.name}
                                                </TableCell>
                                                <TableCell align="right">{row.execution_time}</TableCell>
                                                <TableCell align="right">
                                                    <Button variant="outlined" color="secondary" className={classes.button}>
                                                        Відмінити
                                                </Button>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                </TableBody>
                            </Table>
                        </Paper>
                    </Grid>
                    <Grid item>
                        <Typography gutterBottom variant="h5" component="h2">
                            Прогроз погоди на сьогодні
                            </Typography>

                    </Grid>
                    <Grid item>
                        <Typography gutterBottom variant="h5" component="h2">
                            Погода за останні {weatherData.length} годин
                            </Typography>
                        <Paper className={classes.root}>
                            <Table className={classes.table}>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Час</TableCell>
                                        <TableCell align="right">Температура</TableCell>
                                        <TableCell align="right">Вологість</TableCell>
                                        <TableCell align="right">Погода</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {weatherData.map(row => (
                                            <TableRow key={row.time}>
                                                <TableCell component="th" scope="row">
                                                    {row.time}
                                                </TableCell>
                                                <TableCell align="right">{row.temp}</TableCell>
                                                <TableCell align="right">{row.humidity}</TableCell>
                                                <TableCell align="right">{row.weather}</TableCell>
                                            </TableRow>
                                        ))}
                                </TableBody>
                            </Table>
                        </Paper>
                    </Grid>
                </Grid>
            </>
        );
    }
}
