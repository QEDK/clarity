import React from 'react'

const Header = () => {
    return (
        <>
            <header className='header' data-testid='header'>
                <nav>
                    <div className="logo">Clarity</div>
                    <div className="settings">
                        <ul>
                            <li data-testid='quick-add-task-action' className="settings__add">
                                <button type='button' aria-label='Quick Add Task' onClick={() => console.log("headerclicked")}>+</button>
                            </li>
                        </ul>
                    </div>
                </nav>
            </header>
        </>
    )
}

export default Header
