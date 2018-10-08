import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import ControlCard from '../ControlCard'
import ToolbarAppWeb from '../ToolbarApp'

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
    position:'fixed',
    width:'80px',
    height:'60px',
    bottom:'20px',
    right:'20px',
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
});

class IrrigationForm extends React.Component {
  render() {
  const { classes } = this.props;

  return (
    <React.Fragment>
    <ToolbarAppWeb/>     
      <main className={classes.content_main}>
               <Grid container 
                   spacing={24}
                   direction="row"
                   justify="flex-start"
                   alignItems="flex-start">
                
                <ControlCard />
                <ControlCard />
                <ControlCard />
                <ControlCard />
                <ControlCard />
                <ControlCard />
                <ControlCard />
                <ControlCard />
                <ControlCard />
               </Grid>
                 <Button variant="extendedFab" color="primary" className={classes.button_float}>
        Почати полив
      </Button>
      </main>
    </React.Fragment>
  );
}
}

IrrigationForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(IrrigationForm);