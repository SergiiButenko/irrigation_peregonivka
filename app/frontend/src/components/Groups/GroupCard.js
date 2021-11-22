import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import PageSpinner from '../shared/PageSpinner';
import {webUri} from '../../constants/uri';
import ArrowForwardIos from '@material-ui/icons/ArrowForwardIos';
import { getGroups } from '../../selectors/groups';

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
@connect(mapStateToProps)
export default class GroupCard extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        groupId: PropTypes.string.isRequired,
    };

    redirectToGroup = (id) => (e) => {
        this.props.history.push(webUri.GROUPS(id));
    };

    render() {
        const {classes, loading, groups, groupId} = this.props;

        if (loading) {
            return <PageSpinner/>;
        }
        
        const group = groups[groupId];
        return (
            <Paper
                className={classes.root}
                elevation={1}
                onClick={this.redirectToGroup(group.id)}
            >
                <Grid
                    container
                    spacing={24}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <Grid item xs={8}>
                        <Typography variant="h5" component="h3">
                            {group.name}
                        </Typography>
                        <Typography component="p">
                            {group.description}
                        </Typography>
                    </Grid>
                    <Grid item xs={1}>
                        <ArrowForwardIos />
                    </Grid>
                </Grid>
            </Paper>
        );
    }
}
