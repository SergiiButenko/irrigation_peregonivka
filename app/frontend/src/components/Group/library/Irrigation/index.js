import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';


import NavigationIcon from '@material-ui/icons/Navigation';
import Grid from '@material-ui/core/Grid';
import { Button } from '@material-ui/core';

import { postDeviceTasks } from '../../../../actions/device';
import PageSpinner from '../../../shared/PageSpinner';
import LoadingFailed from '../../../shared/LoadingFailed';
import LineCard from './LineCard';

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
});

const mapStateToProps = (state) => {
    return state;
};

@withStyles(styles)
@withRouter
@connect(mapStateToProps, { postDeviceTasks })
export default class IrrigationMaster extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        group: PropTypes.object.isRequired,
        loading: PropTypes.bool.isRequired,
        groupFetchError: PropTypes.any,
    };

    render() {
        const { classes, loading, groupFetchError, group, match: { params }, postDeviceTasks } = this.props;

        if (loading) {
            return <PageSpinner />;
        }

        if (groupFetchError) {
            return <LoadingFailed errorText={groupFetchError} />;
        }

        return (
            <>
                <Grid container spacing={24}>
                    {
                        Object.keys(group.components).map(function (id, index) {
                            return (
                                <Grid item xs={12}>
                                    <LineCard
                                        acuatorId={group.components[id].id}
                                        groupId={group.id}
                                        key={group.components[id].id} />
                                </Grid>
                            );
                        })
                    }


                    <Grid item xs={12}>
                        <Button 
                        color="primary"
                        variant="extendedFab"
                        aria-label="Delete"
                        className={classes.button}
                        onClick={() => postDeviceTasks(device.id)}>
                            <NavigationIcon className={classes.extendedIcon} />
                            Почати полив
                        </Button>
                    </Grid>
                </Grid>
            </>
        );
    }
}
