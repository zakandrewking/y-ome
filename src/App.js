import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import './App.css'
import GeneList from './GeneList'
import Gene from './Gene'

class App extends Component {
  render () {
    return (
      <div>
        <Route exact path='/' component={GeneList} />
        <Route path='/gene/:locusId' component={Gene} />
      </div>
    )
  }
}

export default App
