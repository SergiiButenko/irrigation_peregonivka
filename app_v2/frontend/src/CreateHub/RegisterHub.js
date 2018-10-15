
import React from 'react';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

function RegisterHub() {
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Зарееструйте Хаб
      </Typography>
      <Grid container spacing={24}>
        <Grid item xs={12} md={6}>
          <TextField required id="cardName" label="Імя" fullWidth />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField required id="cardNumber" label="Ідентифікатор" helperText="Знайдіть його на наклейці на Хабі" fullWidth />
        </Grid>
      </Grid>
    </React.Fragment>
  );
}

export default RegisterHub;