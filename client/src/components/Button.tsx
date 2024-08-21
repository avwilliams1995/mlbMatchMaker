import React from 'react'
import "../styles/Button.css"


type ButtonProps = {
  children: string | React.JSX.Element
  onClick: () => void
}

function Button({children, onClick}: ButtonProps) {
  return (
    <>
      <button onClick={onClick}>
          {children}
        </button>
    </>
  )
}

export default Button