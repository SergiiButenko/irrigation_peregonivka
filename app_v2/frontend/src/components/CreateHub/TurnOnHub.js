import React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

function TurnOnHub() {
    return (
        <React.Fragment>
            <Grid container spacing={24} direction="column">
                <Grid item xs={12} sm={6}>
          Підключіть Хаб по роутера, використовуючи Ethernet кабель та дочекайтеся, поки логотип стане зеленим
                </Grid>
                <Grid item xs={12} sm={6}>
          Cool picture.png
                </Grid>
            </Grid>
        </React.Fragment>
    );
}

export default TurnOnHub;