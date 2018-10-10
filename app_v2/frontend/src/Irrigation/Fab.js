import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import * as actionCreators from '../actions/actionCreators';
import store from '../store';
import * as selectors from '../selectors';
import * as utils from '../Utils';


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
        this.previousValue = null;
    }

  state = {
      active: 0,
  }
  
  
  handleChange = () => {
      let currentValue = selectors.get_lines(store);

      if (this.previousValue !== currentValue) {
          this.previousValue = currentValue;
          this.setButtonState(
              Object.values(currentValue.lines).some((line) => {return line.state == 1})
          );
      }
  }

  componentDidMount() {
      this.unsubscribe = store.subscribe(this.handleChange);
      console.log('Subscribed');
  }
  
  componentWillUnmount() {
      // and unsubscribe later
      console.log('UnSubscribed');
      this.unsubscribe();
  }

  setButtonState = (active) => {  
      this.setState({
          active: active,
      });
  }

  render() {
      const { classes } = this.props;

      return (
          <React.Fragment>
              <Button 
                  disabled={!this.state.active}
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