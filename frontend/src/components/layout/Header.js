import React, { useState } from 'react';
import AddTask from '../AddTask';

const Header = () => {
    const [shouldShowMain, setShouldShowMain] = useState(false)
    const [showQuickAddTask, setShowQuickAddTask] = useState(false)
    return (
        <>
            <header className='header' data-testid='header'>
                <nav>
                    <div className='logo'>
                        Clarity
                    </div>
                    <div className="settings">
                        <ul>
                            <li data-testid='quick-add-task-action' className='settings__add'><button type='button' aria-label='Quick Add Task' onClick={()=>{setShowQuickAddTask(true); setShouldShowMain(true)}} onKeyDown={()=>{setShowQuickAddTask(true); setShouldShowMain(true)}}>+</button></li>
                        </ul>
                    </div>
                </nav>
                <AddTask showAddTaskMain={false} shouldShowMain={shouldShowMain} showQuickAddTask={showQuickAddTask} setShowQuickAddTask={setShowQuickAddTask} />
            </header>
        </>
    )
}

export default Header;