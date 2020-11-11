import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AddTask from '../AddTask';
// import { AiOutlineUser , AiOutlineLogout} from 'react-icons/ai';

const Header = () => {
    const [shouldShowMain, setShouldShowMain] = useState(false)
    const [showQuickAddTask, setShowQuickAddTask] = useState(false)
    return (
        <>
            <header className='header' data-testid='header'>
                <nav>
                    <Link to='/'>
                    <div className='logo'>
                        Clarity
                    </div>
                    </Link>
                    <div className="settings">
                        <ul>
                            <li data-testid='quick-add-task-action' className='settings__add'><button type='button' aria-label='Quick Add Task' onClick={()=>{setShowQuickAddTask(true); setShouldShowMain(true)}} onKeyDown={()=>{setShowQuickAddTask(true); setShouldShowMain(true)}}>+</button></li>
                            {/* <Link to='/login'><li data-testid='login' className='settings__add'><button type='button' aria-label='Login'><AiOutlineUser size={23} style={{'marginTop': '5px'}}/></button></li></Link> */}
                        </ul>
                    </div>
                </nav>
                <AddTask showAddTaskMain={false} shouldShowMain={shouldShowMain} showQuickAddTask={showQuickAddTask} setShowQuickAddTask={setShowQuickAddTask} />
            </header>
        </>
    )
}

export default Header;