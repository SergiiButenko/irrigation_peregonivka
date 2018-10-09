import {createMuiTheme} from '@material-ui/core/styles';
// import 'typeface-roboto';

export const theme = createMuiTheme({
  typography: {
    useNextVariants: true,
  },
  palette: {
        primary: {
            main: '#009688',
        }
  },
});