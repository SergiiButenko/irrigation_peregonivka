import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import Grid from '@material-ui/core/Grid';

import { getGroups } from '../../selectors/groups';
import { fetchGroupComponentsById } from '../../actions/groups';
import PageSpinner from '../shared/PageSpinner';
import LoadingFailed from '../shared/LoadingFailed';
import { webUri } from '../../constants/uri';
import Typography from '@material-ui/core/Typography';

import ArrowBackIosRounded from '@material-ui/icons/ArrowBackIosRounded';
import { group_view_map } from '../../constants/components_mapping';

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
});

const mapStateToProps = (state) => {
    return getGroups(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, { fetchGroupComponentsById })
export default class Group extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        groups: PropTypes.object.isRequired,
        groupFetchError: PropTypes.any,
    };

    componentDidMount() {
        this.props.fetchGroupComponentsById(this.props.match.params.groupId);
    }

    redirectToGroups = () => {
        this.props.history.push(webUri.GROUPS());
    };

    render() {
        const { classes, loading, groupFetchError, groups, match: { params } } = this.props;
        const group = groups[params.groupId];

        if (loading) {
            return <PageSpinner />;
        }

        if (groupFetchError) {
            return <LoadingFailed errorText={groupFetchError} />;
        }

        const Element = group_view_map[group.short_name];        
        return (
            <>
                <Grid container spacing={24}>
                    <Grid item xs={12} onClick={this.redirectToGroups}>
                        <Typography variant="h5" component="h3">
                            <ArrowBackIosRounded /> На попередню сторінку
                        </Typography>
                    </Grid>
                    <Grid item xs={12} key={group.id}>
                        <Element groupId={group.id} loading={true}/>
                    </Grid>
                </Grid>
            </>
        );
    }
}
