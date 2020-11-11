import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/layout/Header';
import Content from './components/layout/Content';
// import Login from './components/layout/Login';
import {ProjectsProvider, SelectedProjectProvider} from './context'

function App() {
  const base_url = process.env.REACT_APP_BASE_URL
  console.log(base_url)
  return (
    <Router>
    <SelectedProjectProvider>
      <ProjectsProvider>
    <main data-testid='application'>
      <Header />
      <Switch>
      <Route exact path='/' component={Content} />
      {/* <Route exact path='/login' component={Login} /> */}
      </Switch>
    </main>
    </ProjectsProvider>
    </SelectedProjectProvider>
    </Router>
  );
}

export default App;
