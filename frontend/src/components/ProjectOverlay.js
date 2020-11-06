import React from 'react'
import {useProjectsValue} from '../context'

const ProjectOverlay = ({setProject, showProjectOverlay, setShowProjectOverlay}) => {
    const {projects} = useProjectsValue()

    return(
        projects && showProjectOverlay && (
            <div className='project-overlay' data-testid='project-overlay'>
                <ul className='project-overlay__list'>
                    {
                        projects.map(project=>(
                            <li key={project.projectId} data-testid='project-overlay-action'>
                                <div  onClick={()=>{
                                setProject(project.projectId)
                                setShowProjectOverlay(false)
                            }} onKeyDown={()=>{
                                setProject(project.projectId)
                                setShowProjectOverlay(false)
                            }} role='button' tabIndex={0} aria-label='Select the journal list' >
                                {project.name}
                                </div>
                            </li>
                        ))
                    }
                </ul>
            </div>
        )
    )
}

export default ProjectOverlay