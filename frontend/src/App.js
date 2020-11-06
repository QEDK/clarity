import React from 'react';
import Header from './components/layout/Header';
import Content from './components/layout/Content';
import {ProjectsProvider, SelectedProjectProvider} from './context'

function App() {
  return (
    <SelectedProjectProvider>
      <ProjectsProvider>
    <main data-testid='application'>
      <Header />
      <Content />
    </main>
    </ProjectsProvider>
    </SelectedProjectProvider>
  );
}

export default App;
