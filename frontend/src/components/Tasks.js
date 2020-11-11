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
    // const { selectedProject } = useSelectedProjectValue()
    // const { projects } = useProjectsValue()
    // const {tasks} = useTasks(selectedProject)
    // const [tasks, setTasks] = useState('')

    // let projectName = ''

    // if (projects && selectedProject && !collatedTasksExist(selectedProject)) {
    //     projectName = getTitle(projects, selectedProject).name
    // }

    // if (collatedTasksExist(selectedProject) && selectedProject) {
    //     projectName = getCollatedTitle(collatedTasks, selectedProject).name
    // }

    // useEffect((event) => {
    //     document.title = `${projectName}: Clarity`
    //     const base_url = process.env.REACT_APP_BASE_URL
    //     const email = "shahpreetk@gmail.com"
    //     axios.get(`${base_url}/get_note/${email}`)
    //         .then(res => {
    //             console.log(res.data)
    //             setTasks(res.data)
    //         })
    //         .catch(err => console.log(err))

    // if (JSON.stringify(allProjects) !== JSON.stringify(projects)){
    //     setProjects(allProjects);
    // });
    render() {
        const {tasks} = this.state
        return (
            <div className='tasks' data-testid='tasks'>

                <ul className='tasks__list'>
                    {
                        tasks.map(task => (
                            <li key={`${task.id}`}>
                                <Checkbox id={task.id} taskDesc={task.task} />
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