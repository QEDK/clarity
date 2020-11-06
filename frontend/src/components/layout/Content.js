import React from 'react';
import Sidebar from './Sidebar';
import Tasks from '../Tasks'

const Content = () => {
    return(
        <section className='content'>
            <Sidebar/>
            <Tasks/>
        </section>
    )
}

export default Content;