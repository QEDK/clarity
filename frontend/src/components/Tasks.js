import React, { Component } from 'react'
// import Checkbox from './Checkbox'
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
                this.setState({
                    tasks,
                })
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
                            let tf_idf_keys = Object.keys(model.tf_idf)
                            console.log("model values = \n", model)
                            return (
                                <>
                                    <li key={`${task.id}`}>
                                        {/* <Checkbox id={task.id} taskDesc={task.task} /> */}
                                        <div>
                                            <h3 style={{ margin: 0, padding: 0, border: 'none' }}>{task.text_journal}</h3>
                                            <br />
                                            <ul>
                                                <li style={{ borderBottom: 'none', padding: 0, margin: 0 }}>
                                                    {tf_idf_keys.map((key, i) => <p key={`${i}`} style={{ color: 'orange', margin: 0, padding: 0 }}>{key}&nbsp;</p>)}
                                                </li>
                                                <li style={{ borderBottom: 'none', padding: 0, margin: 0 }}>
                                                    {model.sentiment.mood.empty > 10 && (
                                                        <p style={{ color: 'grey', margin: 0, padding: 0 }}>
                                                            empty = {model.sentiment.mood.empty}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.sadness > 10 && (
                                                        <p style={{ color: 'red', margin: 0, padding: 0 }}>
                                                            sadness = {model.sentiment.mood.sadness}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.enthusiasm > 10 && (
                                                        <p style={{ color: 'green', margin: 0, padding: 0 }}>
                                                            enthusiasm = {model.sentiment.mood.enthusiasm}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.neutral > 10 && (
                                                        <p style={{ color: 'grey', margin: 0, padding: 0 }}>
                                                            neutral = {model.sentiment.mood.neutral}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.worry > 10 && (
                                                        <p style={{ color: 'red', margin: 0, padding: 0 }}>
                                                            worry = {model.sentiment.mood.worry}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.surprise > 10 && (
                                                        <p style={{ color: 'grey', margin: 0, padding: 0 }}>
                                                            surprise = {model.sentiment.mood.surprise}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.love > 10 && (
                                                        <p style={{ color: 'green', margin: 0, padding: 0 }}>
                                                            love = {model.sentiment.mood.love}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.fun > 10 && (
                                                        <p style={{ color: 'green', margin: 0, padding: 0 }}>
                                                            fun = {model.sentiment.mood.fun}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.hate > 10 && (
                                                        <p style={{ color: 'red', margin: 0, padding: 0 }}>
                                                            hate = {model.sentiment.mood.hate}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.happiness > 10 && (
                                                        <p style={{ color: 'green', margin: 0, padding: 0 }}>
                                                            happiness = {model.sentiment.mood.happiness}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.boredom > 10 && (
                                                        <p style={{ color: 'grey', margin: 0, padding: 0 }}>
                                                            boredom = {model.sentiment.mood.boredom}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.relief > 10 && (
                                                        <p style={{ color: 'green', margin: 0, padding: 0 }}>
                                                            relief = {model.sentiment.mood.relief}
                                                    &nbsp;</p>
                                                    )}
                                                    {model.sentiment.mood.anger > 10 && (
                                                        <p style={{ color: 'red', margin: 0, padding: 0 }}>
                                                            anger = {model.sentiment.mood.anger}
                                                    &nbsp;</p>
                                                    )}
                                                </li>
                                                <li style={{ borderBottom: 'none', padding: 0, margin: 0 }}>
                                                    <p style={{ color: 'blue', margin: 0, padding: 0 }}>Polarity = {model.sentiment.polarity}&nbsp;</p>
                                                    <p style={{ color: 'purple', margin: 0, padding: 0 }}>Subjectivity = {model.sentiment.subjectivity}</p>
                                                </li>
                                            </ul>
                                        </div>
                                    </li>
                                </>
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