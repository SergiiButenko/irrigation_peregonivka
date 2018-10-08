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
      this.boundActionCreators = bindActionCreators(actionCreators, dispatch)
      console.log(this.boundActionCreators)
    }

  state = {
    selected: 0,
    id: -1,
  }

    componentDidMount() {
    let { dispatch } = this.props

    let action = actionCreators.set_state(1, 0)
    dispatch(action)
  }

  toggleSelected = () => {
    let { dispatch } = this.props
    let action = actionCreators.set_state(1, !this.state.selected)
    dispatch(action)
    
    this.setState({
      selected: !this.state.selected,
    });
  };

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
      <Grid item>
      <Card className={classes.card, this.state.selected ? classes.cardSelected : ''}>
        <CardContent className={classes.content}>        
          <Typography className={classes.title} component="h2">
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
          onClick={this.toggleSelected}
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

function mapStateToProps (state) {
  return {
    lines: state
  }
}

export default withStyles(styles)(connect(mapStateToProps)(ControlCard));