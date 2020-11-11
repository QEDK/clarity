import {useState, useEffect} from 'react'
import moment from 'moment'
import {firebase} from '../firebase'
import {collatedTasksExist} from '../helpers'
import axios from 'axios'

export  const useTasks = selectedProject => {
    const [tasks, setTasks] = useState([])
    const [archivedTasks, setArchivedTasks] = useState([])

    useEffect(()=>{
        let unsubscribe = firebase
            .firestore()
            .collection('tasks')
            .where('userId', '==', 'c422780d6077477594639749729eef36');

            unsubscribe =
                selectedProject && !collatedTasksExist(selectedProject)
                    ? (unsubscribe = unsubscribe.where('projectId', '==', selectedProject))
                    : selectedProject === 'TODAY'
                    ? (unsubscribe = unsubscribe.where('date', '==', moment().format('DD/MM/YYYY')))
                    : selectedProject === 'INBOX' || selectedProject === 0
                    ? (unsubscribe = unsubscribe.where('date', '==', ''))
                    : unsubscribe;

        unsubscribe = unsubscribe.onSnapshot(snapshot => {
            const newTasks = snapshot.docs.map(task=>({
                id:task.id,
                ...task.data(),
            }));

            setTasks(
                selectedProject === 'NEXT_7'
                ? newTasks.filter(
                    task=>moment(task.date,'DD-MM-YYYY').diff(moment(), 'days') <= 7 &&
                    task.archived !== true
                )
                : newTasks.filter(task => task.archived !== true)
            );

            setArchivedTasks(newTasks.filter(task=>task.archived!==false))
        });

        return() => unsubscribe()
    },[selectedProject]);

    return {tasks, archivedTasks}
}

export const useProjects = () => {
    const [projects, setProjects] = useState([]);

    useEffect(()=>{
        // firebase
        //     .firestore()
        //     .collection('projects')
        //     .where('userId', '==', 'c422780d6077477594639749729eef36')
        //     .orderBy('projectId')
        //     .get()
        //     .then(snapshot=>{
        //         const allProjects = snapshot.docs.map(project=>({
        //             ...project.data(),
        //             docId:project.id,
        //         }));

        //         if (JSON.stringify(allProjects) !== JSON.stringify(projects)){
        //             setProjects(allProjects);
        //         }
        //     });
        axios.get('https://60a4c101b9b5.ngrok.io/api/get_note/shahpreetk@gmail.com')
            .then(snapshot=>{
                const allProjects = snapshot.docs.map(project=>({
                    ...project.data(),
                    docId:project.id,
                }));

                if (JSON.stringify(allProjects) !== JSON.stringify(projects)){
                    setProjects(allProjects);
                }
            });
    },[projects]);

    return {projects, setProjects};
}