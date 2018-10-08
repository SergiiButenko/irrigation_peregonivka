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