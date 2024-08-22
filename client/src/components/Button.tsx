import React from 'react'
import "../styles/Button.css"


type ButtonProps = {
  children: string | React.JSX.Element
  onClick: () => void
  color?: string
}

function Button({children, onClick, color}: ButtonProps) {
  return (
    <>
      <button onClick={onClick} className={color ? `btn-${color}` : 'btn-default'}>
          {children}
        </button>
    </>
  )
}

export default Button