import React, { Component } from 'react'
// import Checkbox from './Checkbox'
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
            tasks: [],
        };
    }
    componentDidMount(tasks) {
        document.title = 'Clarity'
        const base_url = process.env.REACT_APP_BASE_URL
        const email = "coderaji13@gmail.com"
        axios.get(`${base_url}/get_note/${email}`)
            .then((res) => {
                // console.log(res.data)
                tasks = res.data
                // model_output = JSON.parse(tasks)
                this.setState({
                    tasks,
                })
                // console.table(model_output.ents)
            })
            .catch(err => console.log(err))
    }

    render() {
        const { tasks } = this.state
        return (
            <div className='tasks' data-testid='tasks'>

                <ul className='tasks__list'>
                    {
                        tasks.map((task) => {

                            let model = JSON.parse(JSON.parse(JSON.stringify(task.model_output)))
                            console.log("model sadness = ", model.sentiment.mood.sadness)
                            return (
                                <li key={`${task.id}`}>
                                    <span>{task.text_journal}
                                        <br />
                                        {model.sentiment.mood.sadness}
                                    </span>
                                </li>
                            )
                        })
                    }
                </ul>
                <AddTask />
            </div>
        )
    }
}

export default Tasks;