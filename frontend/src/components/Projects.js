import React, { useState } from 'react';
import { useSelectedProjectValue, useProjectsValue } from '../context';
import IndividiualProject from './IndividualProject';

const Projects = ({ activeValue = null }) => {
    const [active, setActive] = useState(activeValue)
    const { setSelectedProject } = useSelectedProjectValue()
    const { projects } = useProjectsValue()
    return (
        projects &&
        projects.map(project => (
            <li
                key={project.projectId}
                data-doc-id={project.docId}
                data-testid="project-action"
                className={
                    active === project.projectId
                        ? 'active sidebar__project'
                        : 'sidebar__project'
                }>
                <div role='button' aria-label={`Select ${project.name} as the task project`} tabIndex={0} onKeyDown={() => {
                    setActive(project.projectId)
                    setSelectedProject(project.projectId)
                }}
                    onClick={() => {
                        setActive(project.projectId)
                        setSelectedProject(project.projectId)
                    }}>
                    <IndividiualProject project={project} />
                </div>
            </li>
        ))
    )
}

export default Projects;