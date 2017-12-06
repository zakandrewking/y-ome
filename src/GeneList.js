import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { locusIds } from './data/index.json'

class GeneList extends Component {
  render () {
    const divs = locusIds.map(locusId => {
      return (
        <div style={{width: '100%'}} key={locusId}>
          <Link to={`/gene/${locusId}`}>{locusId}</Link>
        </div>
      )
    })
    return (
      <div>
        <h1>GeneList</h1>
        {divs}
      </div>
    )
  }
}

export default GeneList
