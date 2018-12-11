import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';


const styles = theme => ({
    button_float: {
        margin: theme.spacing.unit,
        position: 'fixed',
        width: '80px',
        height: '60px',
        bottom: '20px',
        right: '20px',
    },
});

class Fab extends React.Component {

    state = {
        active: 0,
    };
    // handleChange = () => {
    //     if (this.previousValue !== currentValue) {
    //         this.previousValue = currentValue;
    //         this.setButtonState(
    //             Object.values(currentValue.lines).some((line) => {
    //                 return line.state === 1;
    //             })
    //         );
    //     }
    // };
    // setButtonState = (active) => {
    //     this.setState({
    //         active: active,
    //     });
    // };

    constructor(props) {
        super(props);
        this.previousValue = null;
    }

    componentDidMount() {

    }

    render() {
        const {classes} = this.props;

        return (
            <Button
                disabled={!this.state.active}
                variant="extended"
                color="primary"
                className={classes.button_float}>
                Почати полив
            </Button>
        );
    }
}

Fab.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Fab);