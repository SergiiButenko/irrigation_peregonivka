import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import compose from 'recompose/compose';
import * as actionCreators from '../actions/actionCreators'
import store from '../store'
console.log(actionCreators)

const styles = theme => ({
  button_float: {
    margin: theme.spacing.unit,
    position:'fixed',
    width:'80px',
    height:'60px',
    bottom:'20px',
    right:'20px',
  },
});

class Fab extends React.Component {

  constructor(props) { 
    super(props);  
      console.log("Store is:", store.getState())
    }

  state = {
    active: 0,
  }
  
  
  handleChange = () => {
    let currentValue
    let previousValue = currentValue
    currentValue = store.getState()

    if (previousValue !== currentValue) {
      console.log(
        'Some deep nested property changed from',
        previousValue,
        'to',
        currentValue
      )
    }
  }

  componentDidMount() {
    store.subscribe(this.handleChange)
    console.log("Subscribed")
  }
  

  toggleSelected = () => {  
    this.setState({
      active: !this.state.active,
    });
  };

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
          <Button 
          variant="extendedFab" 
          color="primary" 
          className={classes.button_float}>
          Почати полив
        </Button>
      </React.Fragment>
    );
  }
}

Fab.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Fab);