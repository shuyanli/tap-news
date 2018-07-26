import React from 'react';
import logo from './news-icon.jpeg';
import './App.css';

import NewsPanel from '../NewsPanel/NewsPanel'


class App extends React.Component {
    render () {
        return (
            <div>
                <img className='logo' src={logo} alt = 'logo' />
                <div className='conatiner'>
                   <NewsPanel/>
                </div>
            </div>
        );
    }
}

export default App;