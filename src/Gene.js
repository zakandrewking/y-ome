import React, { Component } from 'react'
import { Link } from 'react-router-dom'

class Gene extends Component {
  render () {
    console.log(this)
    const { locusId } = this.props.match.params
    return (
      <div>
        <h1>Gene: { locusId }</h1>
        <Link to='/'>Home</Link>
      </div>
    )
  }
}

export default Gene
