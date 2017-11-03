import React, { Component } from 'react'
import './App.css'

import { locusIds } from './data/index.json'

class App extends Component {
  render () {
    const divs = locusIds.map(locusId => {
      return <div style={{width: '100%'}}>{locusId}</div>
    })
    return <div>{divs}</div>
  }
}

export default App
