import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';


import NavigationIcon from '@material-ui/icons/Navigation';

import Grid from '@material-ui/core/Grid';
import { Button } from '@material-ui/core';
import Zoom from '@material-ui/core/Zoom';

import { postDeviceTasks } from '../../../../actions/groups';
import PageSpinner from '../../../shared/PageSpinner';
import LoadingFailed from '../../../shared/LoadingFailed';
import { components_mapping } from '../../../../constants/components_mapping';
import { getGroups } from '../../../../selectors/groups';

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
    return getGroups(state);
};

@withStyles(styles)
@withRouter
@connect(mapStateToProps, { postDeviceTasks })
export default class CesspoolMaster extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        group: PropTypes.object.isRequired,
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
                            const component = group.components[id]
                            const Element = components_mapping[component.usage_type][component.category][component.version]
                            return (
                                <Grid item xs={12}>
                                    <Element
                                        componentId={component.id}
                                        groupId={group.id}
                                        key={component.id} />
                                </Grid>
                            );
                        })
                    }
                </Grid>
            </>
        );
    }
}
