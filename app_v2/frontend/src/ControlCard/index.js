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
import * as utils from '../Utils'
import Slider from '@material-ui/lab/Slider';
import Collapse from '@material-ui/core/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import AccessTime from '@material-ui/icons/AccessTime';
import Iso from '@material-ui/icons/Iso';


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
  title: {
    marginBottom: 5,
    flex: 1,
    display: 'inline',
  },
  pos: {
    marginBottom: 12,
  },
  button: {
    margin: theme.spacing.unit * 0,
    flex: 1,
  },
  slider_root: {
    width: '100%',
  },
  slider: {
    padding: '22px 0px',

  },
  minutes: {
    marginBottom: 5,
    marginLeft: '3rem',
    flex: 1,
    display: 'inline',
  },
  expandMore: {
    transform: 'rotate(180deg)',
    transition: '300ms transform',
  },
  expandMore_selected: {
    transform: 'rotate(360deg)',
    transition: '300ms transform',
  },
  thumbIcon: {
    width: '30px',
    height: '50px',
    marginTop: '-20px',
  },
});

class ControlCard extends React.Component {

    constructor(props) { 
      super(props);  
      const {dispatch} = props;
      this.boundActionCreators = bindActionCreators(actionCreators, dispatch)
      this.id = utils.guid()

    }

  state = {
    selected: 0,
    value_minutes: 15,
    value_qnt: 2,
    collapsed: false,
  }

  componentDidMount() {
    let { dispatch } = this.props

    let action = actionCreators.add_card(this.id)
    dispatch(action)
  }

  componentWillUnmount() {
    // let { dispatch } = this.props

    // let action = actionCreators.remove_card(this.id)
    // dispatch(action)
  }

  toggleSelected = () => {
    let { dispatch } = this.props
    let action = actionCreators.set_state(this.id, !this.state.selected)
    dispatch(action)
    
    this.setState({
      selected: !this.state.selected,
    });
  }

  setSelected = () => {
    let { dispatch } = this.props
    let action = actionCreators.set_state(this.id, 1)
    dispatch(action)
    
    this.setState({
      selected: 1,
    });
  }

  handleCollapse = () => {
    this.setState(state => ({ collapsed: !state.collapsed }));
  }

  handleChangeMinutes = (event, value_minutes) => {
    this.setState({ value_minutes });
  }

  handleChangeQnt = (event, value_qnt) => {
    this.setState({ value_qnt });
  }

  render() {
    const { classes } = this.props;
    const { value_minutes, value_qnt, selected, collapsed } = this.state;
  
    return (
      <React.Fragment>
      <Grid item>
        <Card className={classes.card, this.state.selected ? classes.cardSelected : ''}>
          <CardContent className={classes.content}>        
            <div 
                onClick={this.handleCollapse}
                // onMouseEnter={() => {
                //   document.body.style.cursor = "pointer";
                // }}
                // onMouseLeave={() => {
                //   document.body.style.cursor = "default";
                // }}
                >
            <Typography className={classes.title} variant="h5" align='left'>
              Томати
            </Typography>
            <Typography className={classes.minutes} variant="button" align='right'>
              {value_qnt} {value_qnt == 1 ? 'раз, ' : 'раза по'} {value_minutes} хв
            </Typography>
            <ExpandMoreIcon className={collapsed == 1 ? classes.expandMore_selected : classes.expandMore}/>
            </div>

            <Collapse in={collapsed}>
            
            <div className={classes.slider_root}>
            <AccessTime/>
              <Slider
                classes={{ container: classes.slider }}
                value={value_minutes}
                min={10}
                max={20}
                step={5}
                onChange={this.handleChangeMinutes}
                onDragStart={this.setSelected}
          //       thumb={
          //   <AccessTime className={classes.thumbIcon}/>
          // }
              />
            <Iso/>
              <Slider
                classes={{ container: classes.slider }}
                value={value_qnt}
                min={1}
                max={3}
                step={1}
                onChange={this.handleChangeQnt}
                onDragStart={this.setSelected}
          //       thumb={
          //   <Iso className={classes.thumbIcon}/>
          // }
              />
            </div>
          </Collapse>
          </CardContent>
          <CardActions>
          <Button 
          color="primary" 
          className={classes.button}
          onClick={this.toggleSelected}
          >
          {selected == 1 ? 'Не поливати' : 'Обрати' }
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