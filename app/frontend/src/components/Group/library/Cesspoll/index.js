import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import Grid from '@material-ui/core/Grid';
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
        groupId: PropTypes.string.isRequired,
        groupFetchError: PropTypes.any,
    };

    render() {
        const { classes, loading, groupFetchError, groups, groupId, match: { params }, postDeviceTasks } = this.props;

        if (loading) {
            return <PageSpinner />;
        }

        if (groupFetchError) {
            return <LoadingFailed errorText={groupFetchError} />;
        }

        const group = groups[groupId];
        return (
            <>
                <Grid container spacing={24}>
                    {
                        Object.keys(group.components).map(function (id, index) {
                            const component = group.components[id];
                            const Element = components_mapping[group.short_name][component.category][component.version];
                            if (!Element) {
                                return;
                            }
                            
                            return (
                                <Grid item xs={12} key={component.id} >
                                    <Element
                                        componentId={component.id}
                                        groupId={group.id}
                                    />
                                </Grid>
                            );
                        })
                    }
                </Grid>
            </>
        );
    }
}
