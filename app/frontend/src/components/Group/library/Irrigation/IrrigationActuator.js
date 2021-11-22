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
import Iso from '@material-ui/icons/Iso';
import Button from '@material-ui/core/Button';


import connect from 'react-redux/es/connect/connect';
import {
    toggleSelection,
    setSelected,
    changeSettings
} from '../../../../actions/groups';
import { getGroups } from '../../../../selectors/groups';
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
    cardSelected: {
        boxShadow: '0 0 0 3px #8dbdf7',
        background: '#dae7f7',
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
    return getGroups(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, { toggleSelection, setSelected, changeSettings })
export default class IrrigationActuator extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        groups: PropTypes.object.isRequired,
        componentId: PropTypes.string.isRequired,
        groupId: PropTypes.string.isRequired,
    };

    state = {
        collapsed: false,
    };

    handleCollapse = () => {
        this.setState(state => ({ collapsed: !state.collapsed }));
    };

    handleChangeMinutes = (event, value_minutes) => {
        this.props.changeSettings(
            this.props.groupId,
            this.props.componentId,
            'minutes',
            value_minutes
            );
    };

    handleChangeQnt = (event, value_qnt) => {
        this.props.changeSettings(
            this.props.groupId,
            this.props.componentId,
            'quantity',
            value_qnt
            );
    };

    handleStartDrag = (event) => {
        this.props.setSelected(
            this.props.groupId,
            this.props.componentId,
            );
    };



    render() {
        const { componentId, groupId, groups, classes, toggleSelection } = this.props;
        const { collapsed } = this.state;

        const actuator = groups[groupId].components[componentId];

        actuator.selected = !!actuator.selected || false;
        const minutes = actuator.settings.minutes;
        const quantity = actuator.settings.quantity;

        return (
            <Card className={classNames(classes.card, actuator.selected && classes.cardSelected)}>
                <CardContent className={classes.content}>
                    <Grid item
                        container
                        direction="row"
                        spacing={16}
                        >
                        <Grid item>
                            <Typography gutterBottom variant="h5" component="h2">
                                {actuator.name}
                            </Typography>
                        </Grid>
                    </Grid>
                    <Grid item container direction="row" spacing={16} onClick={this.handleCollapse} justify="flex-end">
                        <Grid item>
                            <Typography component="p">Полити {quantity} {quantity === 1 ? 'раз, ' : 'раза по'} {minutes} хв</Typography>
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
                                    value={minutes}
                                    min={5}
                                    max={30}
                                    step={5}
                                    onChange={this.handleChangeMinutes}
                                    onDragEnd={this.handleStartDrag}
                                />
                            </Grid>
                        </Grid>
                        <Grid item container direction="row" spacing={16} justify="center"
                            alignItems="center">
                            <Grid item xs>
                                <Iso />
                            </Grid>
                            <Grid item xs={10}>
                                <Slider
                                    classes={{ container: classes.slider }}
                                    value={quantity}
                                    min={1}
                                    max={4}
                                    step={1}
                                    onChange={this.handleChangeQnt}
                                    onDragEnd={this.handleStartDrag}
                                />
                            </Grid>
                        </Grid>
                    </Collapse>
                </CardContent>

                <CardActions
                    onClick={() => toggleSelection(groupId, componentId)}
                >
                    <Button
                        color="primary"
                        className={classes.button}
                    >
                        {actuator.selected ? 'Не поливати' : 'Обрати'}
                    </Button>
                </CardActions>
            </Card>
        );
    }
}