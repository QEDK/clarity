import React, { useState, useEffect, Component } from 'react'
import Checkbox from './Checkbox'
// import {useTasks} from '../hooks'
// import { collatedTasks } from '../constants'
// import { getTitle, getCollatedTitle, collatedTasksExist } from '../helpers'
// import { useSelectedProjectValue, useProjectsValue } from '../context'
import AddTask from './AddTask'
import axios from 'axios'

class Tasks extends Component {
    constructor() {
        super();
        this.state = {
            tasks: []
        };
    }
    componentDidMount(tasks) {
        document.title = 'Clarity'
        const base_url = process.env.REACT_APP_BASE_URL
        const email = "shahpreetk@gmail.com"
        axios.get(`${base_url}/get_note/${email}`)
            .then((res) => {
                console.log(res.data)
                tasks = res.data
                this.setState({
                    tasks
                })
            })
            .catch(err => console.log(err))
    }

    render() {
        const {tasks} = this.state
        return (
            <div className='tasks' data-testid='tasks'>

                <ul className='tasks__list'>
                    {
                        tasks.map(task => (
                            <li key={`${task.id}`}>
                                {/* <Checkbox id={task.id} taskDesc={task.task} /> */}
                                <span>{task.text_journal}</span>
                            </li>
                        ))
                    }
                </ul>
                <AddTask />
            </div>
        )
    }
}

export default Tasks;