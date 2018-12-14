import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import {connect} from 'react-redux';

import Grid from '@material-ui/core/Grid';
import Fab from './Fab';
import ControlCard from '../ControlCard/index';
import {getIrrigationLines} from '../../selectors/lines';
import {fetchLines} from '../../actions/card';
import PageSpinner from '../shared/PageSpinner';
import LoadingFailed from '../shared/LoadingFailed';
import {LINE_TYPE} from '../../constants/lines';

const styles = theme => ({
    card: {
        minWidth: 275,
        marginBottom: theme.spacing.unit,
    },
    content: {
        minWidth: 275,
        marginBottom: 0,
        paddingBottom: theme.spacing.unit - 8,
    },
    title: {
        marginBottom: 5,
        fontSize: '1.5rem',
    },
    pos: {
        marginBottom: 12,
    },
    button_float: {
        margin: theme.spacing.unit,
        position: 'fixed',
        width: '80px',
        height: '60px',
        bottom: '20px',
        right: '20px',
    },
    extendedIcon: {
        marginRight: theme.spacing.unit,
    },
    content_main: {
        flexGrow: 1,
        padding: theme.spacing.unit * 3,
        height: '100vh',
        overflow: 'auto',
    },
    appBarSpacer: theme.mixins.toolbar,
    root: {
        display: 'flex',
    },
});

const mapStateToProps = (state) => {
    return getIrrigationLines(state);
};
@withStyles(styles)
@connect(mapStateToProps, {fetchLines})
export default class Irrigation extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        lines: PropTypes.array.isRequired,
        loading: PropTypes.bool.isRequired,
        lineFetchError: PropTypes.string,
    };

    constructor(props) {
        super(props);

        this.lineType = LINE_TYPE.IRRIGATION;
    }

    componentWillMount() {
        this.props.fetchLines(this.lineType);
    }

    render() {
        const {classes, loading, lineFetchError, lines} = this.props;

        if (loading) {
            return <PageSpinner/>;
        }

        if (lineFetchError) {
            return <LoadingFailed errorText={lineFetchError}/>;
        }

        return (
            <>
                <Grid container
                    spacing={8}>
                    <Grid item>
                        <ControlCard/>
                    </Grid>
                    <Grid item>
                        <ControlCard/>
                    </Grid><Grid item>
                        <ControlCard/>
                    </Grid><Grid item>
                        <ControlCard/>
                    </Grid><Grid item>
                        <ControlCard/>
                    </Grid><Grid item>
                        <ControlCard/>
                    </Grid><Grid item>
                        <ControlCard/>
                    </Grid>
                </Grid>
                <Fab/>
            </>
        );
    }
}
