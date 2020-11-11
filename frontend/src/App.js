import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/layout/Header';
import Content from './components/layout/Content';
// import Login from './components/layout/Login';
import {ProjectsProvider, SelectedProjectProvider} from './context'

function App() {
  return (
    <Router>
    <SelectedProjectProvider>
      <ProjectsProvider>
    <main data-testid='application'>
      <Header />
      <Switch>
      <Route exact path='/' component={Content} />
      </Switch>
    </main>
    </ProjectsProvider>
    </SelectedProjectProvider>
    </Router>
  );
}

export default App;
