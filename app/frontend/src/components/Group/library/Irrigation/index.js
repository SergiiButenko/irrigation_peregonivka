import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';


import NavigationIcon from '@material-ui/icons/Navigation';

import Grid from '@material-ui/core/Grid';
import { Button } from '@material-ui/core';
import Zoom from '@material-ui/core/Zoom';

import { postDeviceTasks } from '../../../../actions/device';
import PageSpinner from '../../../shared/PageSpinner';
import LoadingFailed from '../../../shared/LoadingFailed';
import { components_mapping } from '../../../../constants/components_mapping';

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
    fab: {
        position: 'absolute',
        bottom: theme.spacing.unit * 2,
        right: theme.spacing.unit * 2,
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

        const transitionDuration = {
            enter: 100,
            exit: 100,
        };

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
                            const component = group.components
                            const Element = components_mapping[component.usage_type][component.category][component.version]
                            return (
                                <Grid item xs={12}>
                                    <Element
                                        componentId={group.components[id].id}
                                        groupId={group.id}
                                        key={group.components[id].id} />
                                </Grid>
                            );
                        })
                    }
                </Grid>
                <Zoom
                    key="primary"
                    in="true"
                    timeout={transitionDuration}
                    unmountOnExit
                >
                    <Button variant="fab" className={classes.fab} color="primary">
                        <NavigationIcon />
                    </Button>
                </Zoom>
            </>
        );
    }
}
