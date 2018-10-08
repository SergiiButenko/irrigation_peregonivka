import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
//import ControlCard from '../ControlCard'
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
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
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
});

class IrrigationForm extends React.Component {
// <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
//                   <ControlCard />
  render() {
  const { classes } = this.props;

  return (
    <React.Fragment>
     <div className={classes.grid_root}>
     <ToolbarAppWeb/>
               <Grid container 
                   spacing={24}
                   direction="row"
                   justify="flex-start"
                   alignItems="flex-start">
                  
                  
               </Grid>
                 <Button variant="extendedFab" color="primary" className={classes.button_float}>
        Почати полив
      </Button>
    </div>
    </React.Fragment>
  );
}
}

IrrigationForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(IrrigationForm);