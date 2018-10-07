import React from 'react';
import {Provider} from 'react-redux'
import ReactDOM from 'react-dom';
import ToolbarAppWeb from './ToolbarApp/Web'
import ToolbarAppMobile from './ToolbarApp/Mobile'
import ControlCard from './ControlCard'
import store from './js/store'

const title = 'My Minimal React Webpack Babel Setup';

function isMobile() {
   if( navigator.userAgent.match(/Android/i)
 || navigator.userAgent.match(/webOS/i)
 || navigator.userAgent.match(/iPhone/i)
 || navigator.userAgent.match(/iPad/i)
 || navigator.userAgent.match(/iPod/i)
 || navigator.userAgent.match(/BlackBerry/i)
 || navigator.userAgent.match(/Windows Phone/i)
 ){
    return true;
  }
 else {
    return false;
  }
}


ReactDOM.render(
	 <Provider store={store}>
        <ToolbarAppWeb />
     </Provider>
 ,
document.getElementById('app')
);

module.hot.accept();