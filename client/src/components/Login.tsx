import React, { useRef, useState } from 'react'
import '../styles/Login.css'
import Button from './Button'
import Spinner from './Spinner'

function Login() {
  const userRef = useRef<HTMLInputElement | null>(null)
  const pwRef = useRef<HTMLInputElement | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = () => {
    setIsLoading(true)
    const username = userRef.current?.value || ""
    const pw = pwRef.current?.value || ""
    const formData = {username, pw}

    try {
      setTimeout(()=> {
        setIsLoading(false)
      }, 4000)
    } catch(err) {
      console.log(err)
    }
    return
  }

  return (
    <div>
      <h1>Welcome to MLB Match Maker!</h1>
      <form onSubmit={(e)=> e.preventDefault}>
        <label>
          Username:
        </label>
        <input type='text' ref={userRef}/>
        <label>
          Password:
        </label>
        <input type='text' ref={pwRef}/>
        <Button onClick={handleSubmit}>{isLoading ? <Spinner size=''/>  : "Submit"}</Button>
      </form>
    </div>
  )
}

export default Login