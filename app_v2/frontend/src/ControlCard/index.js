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
import * as utils from '../Utils';
import Slider from '@material-ui/lab/Slider';
import Collapse from '@material-ui/core/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import AccessTime from '@material-ui/icons/AccessTime';
import Iso from '@material-ui/icons/Iso';
import Avatar from '@material-ui/core/Avatar';
import deepPurple from '@material-ui/core/colors/deepPurple';




const styles = theme => ({
    card: {
        minWidth: 275,
        marginBottom: theme.spacing.unit,
    },
    cardSelected: {
        boxShadow: '0 0 0 3px #8dbdf7',
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
        width: '10%',
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
        transform: 'rotate(360deg)',
        transition: '300ms transform',
    },
    expandMore_selected: {
        transform: 'rotate(180deg)',
        transition: '300ms transform',
    },
    avatar: {
        margin: 10,
    },
    purpleAvatar: {
        margin: 10,
        color: '#fff',
        backgroundColor: deepPurple[500],
    },
    row: {
        display: 'flex',
        justifyContent: 'center',
    },
    header_grid: {
    display: '-webkit-inline-box;',
  },
});

class ControlCard extends React.Component {

    constructor(props) { 
        super(props);  
        const {dispatch} = props;
        this.boundActionCreators = bindActionCreators(actionCreators, dispatch);
        this.id = utils.guid();

    }

  state = {
      selected: 0,
      value_minutes: 15,
      value_qnt: 2,
      collapsed: false,
  }

  componentDidMount() {
      let { dispatch } = this.props;

      let action = actionCreators.add_card(this.id);
      dispatch(action);
  }

  componentWillUnmount() {
      // let { dispatch } = this.props

      // let action = actionCreators.remove_card(this.id)
      // dispatch(action)
  }

  toggleSelected = () => {
      let { dispatch } = this.props;
      let action = actionCreators.set_state(this.id, !this.state.selected);
      dispatch(action);
    
      this.setState({
          selected: !this.state.selected,
      });
  }

  setSelected = () => {
      let { dispatch } = this.props;
      let action = actionCreators.set_state(this.id, 1);
      dispatch(action);
    
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
                          
                            
                              <Grid item xs container direction="row" spacing={24} className={classes.header_grid}>
                                  <Grid item>
                                      <Typography xs gutterBottom variant="h4">
                Томати
                                      </Typography>
                                  </Grid>
                                  
                                  <Grid item xs container direction="row" spacing={24} justify="flex-end"
  alignItems="center"
>
                                  <Grid item md={8} onClick={this.handleCollapse}>
                                      <Typography variant="subtitle1">{value_qnt} {value_qnt == 1 ? 'раз, ' : 'раза по'} {value_minutes} хв</Typography>
                                  </Grid>
                                  <Grid item xs onClick={this.handleCollapse}>
                                      <ExpandMoreIcon className={collapsed == 1 ? classes.expandMore_selected : classes.expandMore}/>
                                  </Grid>
                                  </Grid>
                              </Grid>

                              <Grid item xs container direction="column" spacing={16}>
                                  <Grid item xs>
                                      <Typography gutterBottom >Наступний полив: Завтра, 22:00</Typography>
                                  </Grid>
                                  <Grid item>
                                      <Collapse in={collapsed}>
                                          <Grid item>
                                              <AccessTime/>
                                          </Grid>
                                          <Grid item>
                                              <Slider
                                                  classes={{ container: classes.slider }}
                                                  value={value_minutes}
                                                  min={10}
                                                  max={20}
                                                  step={5}
                                                  onChange={this.handleChangeMinutes}
                                                  onDragStart={this.setSelected}
                                              />
                                          </Grid>
                                          <Iso/>
                                          <Grid item>
                                              <Slider
                                                  classes={{ container: classes.slider }}
                                                  value={value_qnt}
                                                  min={1}
                                                  max={3}
                                                  step={1}
                                                  onChange={this.handleChangeQnt}
                                                  onDragStart={this.setSelected}
                                              />
                                          </Grid>
                                      </Collapse>
                                  </Grid>
                              </Grid>
                          
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
    };
}

export default withStyles(styles)(connect(mapStateToProps)(ControlCard));
