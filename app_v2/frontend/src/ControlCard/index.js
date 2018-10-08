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
import * as actionCreators from './actionCreators'

console.log(actionCreators)

const styles = theme => ({
  card: {
    minWidth: 275,
    marginBottom: theme.spacing.unit,
  },
  cardSelected: {
    border: '2px solid #8dbdf7',
    background: '#dae7f7',
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
  button: {
    margin: theme.spacing.unit * 0,
    flex: 1,
  },
});

class ControlCard extends React.Component {

    constructor(props) { 
      super(props);  
      const {dispatch} = props;
      // Here's a good use case for bindActionCreators:
      // You want a child component to be completely unaware of Redux.
      // We create bound versions of these functions now so we can
      // pass them down to our child later.
      this.boundActionCreators = bindActionCreators(actionCreators, dispatch)
      console.log(this.boundActionCreators)
      // {
      //   addTodo: Function,
      //   removeTodo: Function
      // }
    }

  componentDidMount() {
    // Injected by react-redux:
    let { dispatch } = this.props
    // Note: this won't work:
    // TodoActionCreators.addTodo('Use Redux')
    // You're just calling a function that creates an action.
    // You must dispatch the action, too!
    // This will work:
    let action = actionCreators.selectCard(1)
    dispatch(action)
  }

  state = {
    selected: false
  }

  toggleSelected = () => {
    this.setState({
      selected: !this.state.selected,
    });
  };

  render() {
    const { classes } = this.props;
    //<Card className={classNames(classes.card, this.state.selected && classes.cardSelected)}>

    return (
      <React.Fragment>
      <Grid item>
      <Card className={classes.card, this.state.selected ? classes.cardSelected : ''}>
        <CardContent className={classes.content}>        
          <Typography className={classes.title} variant="headline" component="h2">
            Томати
          </Typography>
          <Typography component="p">
            Наступний полив: завтра, 22:00
          </Typography>
        </CardContent>
        <CardActions>
          <Button 
          color="primary" 
          className={classes.button}
          onClick={() => this.toggleSelected()}
          >
          Обрати
        </Button>
        </CardActions>
      </Card>
      </Grid>
      </React.Fragment>
    );
  }
}

ControlCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default compose(
  withStyles(styles, {
    name: 'ControlCard',
  }),
  connect(state => ({ classes: state.classes }))
)(ControlCard);

export default withStyles(styles)(connect(state => ({ classes: state.classes }))(ControlCard));