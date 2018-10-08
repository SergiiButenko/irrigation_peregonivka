import {createMuiTheme} from '@material-ui/core/styles';

export const theme = createMuiTheme({
	 typography: {
    useNextVariants: true,
  },
    palette: {
        primary: {
            main: '#a31919',
        },
        secondary: {
            main: 'rgb(55, 46, 142)',
        },
    },
});