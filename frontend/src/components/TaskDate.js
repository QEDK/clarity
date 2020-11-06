import React from 'react'
import moment from 'moment';
import { FaSpaceShuttle, FaSun } from 'react-icons/fa'

const TaskDate = ({setTaskDate, showTaskDate, setShowTaskDate}) => showTaskDate && (
    <div className='task-date' data-testid='task-date-overlay'>
        <ul className='task-date__list'>
            <li data-testid='task-date-overlay'>
                <div onClick={()=>{
                setShowTaskDate(false)
                setTaskDate(moment().format('DD/MM/YYYY'))
            }} onKeyDown={()=>{
                setShowTaskDate(false)
                setTaskDate(moment().format('DD/MM/YYYY'))
            }} role='button' tabIndex={0} aria-label='Select today as the task date' ><span><FaSpaceShuttle /></span>
                <span>&nbsp;&nbsp;Today</span></div>
            </li>
            <li data-testid='task-date-tomorrow'>
                <div onClick={()=>{
                setShowTaskDate(false)
                setTaskDate(moment().add(1,'day').format('DD/MM/YYYY'))
            }} onKeyDown={()=>{
                setShowTaskDate(false)
                setTaskDate(moment().add(1,'day').format('DD/MM/YYYY'))
            }} role='button' tabIndex={0} aria-label='Select tomorrow as the task date' ><span><FaSun /></span>
                <span>&nbsp;&nbsp;Tomorrow</span></div>
            </li>
        </ul>
    </div>
)

export default TaskDate