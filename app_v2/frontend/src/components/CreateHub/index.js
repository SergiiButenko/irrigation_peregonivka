import React from 'react';
import PropTypes from 'prop-types';
import withStyles from '@material-ui/core/styles/withStyles';
import Paper from '@material-ui/core/Paper';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import TurnOnHub from './TurnOnHub';
import RegisterHub from './RegisterHub';
import AddDevice from './AddDevice';
import ToolbarAppWeb from '../ToolbarApp/index';

const styles = theme => ({
    appBar: {
        position: 'relative',
    },
    layout: {
        width: 'auto',
        marginLeft: theme.spacing.unit * 2,
        marginRight: theme.spacing.unit * 2,
        [theme.breakpoints.up(600 + theme.spacing.unit * 2 * 2)]: {
            width: 600,
            marginLeft: 'auto',
            marginRight: 'auto',
        },
    },
    paper: {
        marginTop: theme.spacing.unit * 3,
        marginBottom: theme.spacing.unit * 3,
        padding: theme.spacing.unit * 2,
        [theme.breakpoints.up(600 + theme.spacing.unit * 3 * 2)]: {
            marginTop: theme.spacing.unit * 6,
            marginBottom: theme.spacing.unit * 6,
            padding: theme.spacing.unit * 3,
        },
    },
    stepper: {
        padding: `${theme.spacing.unit * 3}px 0 ${theme.spacing.unit * 5}px`,
    },
    buttons: {
        display: 'flex',
        justifyContent: 'flex-end',
    },
    button: {
        marginTop: theme.spacing.unit * 3,
        marginLeft: theme.spacing.unit,
    },
});

const steps = ['Підключіть хаб до мережі', 'Зареєструйте Хаб', 'Додайте пристрої'];

function getStepContent(step) {
    switch (step) {
    case 0:
        return <TurnOnHub />;
    case 1:
        return <RegisterHub />;
    case 2:
        return <AddDevice />;
    default:
        throw new Error('Unknown step');
    }
}

class CreateHub extends React.Component {
  state = {
      activeStep: 0,
  };

  handleNext = () => {
      this.setState(state => ({
          activeStep: state.activeStep + 1,
      }));
  };

  handleBack = () => {
      this.setState(state => ({
          activeStep: state.activeStep - 1,
      }));
  };

  handleReset = () => {
      this.setState({
          activeStep: 0,
      });
  };

  render() {
      const { classes } = this.props;
      const { activeStep } = this.state;

      return (
          <React.Fragment>
              <div className={styles.root}>
                  <ToolbarAppWeb> 
                      <Paper className={classes.paper}>
                          <Typography component="h1" variant="h4" align="center">
              Додайте Хаб
                          </Typography>
                          <Stepper activeStep={activeStep} className={classes.stepper}>
                              {steps.map(label => (
                                  <Step key={label}>
                                      <StepLabel>{label}</StepLabel>
                                  </Step>
                              ))}
                          </Stepper>
                          <React.Fragment>
                              {
                                  <React.Fragment>
                                      {getStepContent(activeStep)}
                                      <div className={classes.buttons}>
                                          {activeStep !== 0 && (
                                              <Button onClick={this.handleBack} className={classes.button}>
                        Назад
                                              </Button>
                                          )}
                                          <Button
                                              variant="contained"
                                              color="primary"
                                              onClick={this.handleNext}
                                              className={classes.button}
                                          >
                                              {activeStep === steps.length - 1 ? 'Додати Пристрої...' : 'Далі'}
                                          </Button>
                                      </div>
                                  </React.Fragment>
                              }
                          </React.Fragment>
                      </Paper>
        
                  </ToolbarAppWeb>
              </div>
          </React.Fragment>
      );
  }
}

CreateHub.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CreateHub);