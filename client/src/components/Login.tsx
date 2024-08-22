import React, { useRef, useReducer } from "react";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendEmailVerification,
  sendPasswordResetEmail,
  setPersistence,
  browserLocalPersistence,
} from "firebase/auth";
import { auth } from "../firebase";
import "../styles/Login.css";
import Button from "./Button";
import Spinner from "./Spinner";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const initialState = {
  isLogin: true,
  isLoading: false,
  error: null,
  resend: false,
  forgotPassword: false,
};

function reducer(state: any, action: any) {
  switch (action.type) {
    case "SET_LOADING":
      return { ...state, isLoading: action.payload };
    case "SET_ERROR":
      return { ...state, error: action.payload };
    case "SET_RESEND":
      return { ...state, resend: action.payload };
    case "TOGGLE_LOGIN_MODE":
      return { ...state, isLogin: !state.isLogin };
    case "TOGGLE_FORGOT_PASSWORD":
      return { ...state, forgotPassword: !state.forgotPassword };
    default:
      return state;
  }
}

function Login() {
  const userRef = useRef<HTMLInputElement | null>(null);
  const pwRef = useRef<HTMLInputElement | null>(null);
  const [state, dispatch] = useReducer(reducer, initialState);
  const navigate = useNavigate();
  const { setCurrentUser } = useAuth();

  const handleLoginSubmit = async () => {
    dispatch({ type: "SET_LOADING", payload: true });
    dispatch({ type: "SET_ERROR", payload: null });
    dispatch({ type: "SET_RESEND", payload: false });
    const username = userRef.current?.value || "";
    const pw = pwRef.current?.value || "";

    try {
      await setPersistence(auth, browserLocalPersistence);
      const userCredential = await signInWithEmailAndPassword(
        auth,
        username,
        pw
      );
      const user = userCredential.user;
      if (user.emailVerified) {
        setCurrentUser({ email: user.email || "" });
        navigate("/");
      } else {
        dispatch({
          type: "SET_ERROR",
          payload: "Please verify your email before logging in.",
        });
        dispatch({ type: "SET_RESEND", payload: true });
      }
    } catch (err) {
      console.log(err);
      dispatch({
        type: "SET_ERROR",
        payload:
          "Failed to log in. Please check your credentials and try again.",
      });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  };

  const handleSignupSubmit = async () => {
    dispatch({ type: "SET_LOADING", payload: true });
    dispatch({ type: "SET_ERROR", payload: null });
    const username = userRef.current?.value || "";
    const pw = pwRef.current?.value || "";

    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        username,
        pw
      );
      const user = userCredential.user;
      await sendEmailVerification(user);
      dispatch({ type: "TOGGLE_LOGIN_MODE" });
      alert(
        "Sign up successful! Please check your email to verify your account before logging in."
      );
    } catch (err: any) {
      console.log(err.code);
      let errorMessage =
        "Failed to sign up. Please check your credentials and try again.";
      if (err.code === "auth/invalid-email") {
        errorMessage = "Invalid email address. Please enter a valid email.";
      } else if (err.code === "auth/email-already-in-use") {
        errorMessage =
          "This email is already in use. Please use a different email or log in.";
      } else if (err.code === "auth/weak-password") {
        errorMessage =
          "Password is too weak. Please enter a stronger password.";
      }
      dispatch({ type: "SET_ERROR", payload: errorMessage });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  };

  const handleResendVerification = async () => {
    dispatch({ type: "SET_ERROR", payload: null });
    if (auth.currentUser) {
      await sendEmailVerification(auth.currentUser);
      alert("Verification email sent! Please check your inbox.");
      dispatch({ type: "TOGGLE_LOGIN_MODE" });
      dispatch({ type: "SET_RESEND", payload: false });
    }
  };

  const handlePasswordReset = async () => {
    dispatch({ type: "SET_ERROR", payload: null });
    const email = userRef.current?.value || "";

    try {
      await sendPasswordResetEmail(auth, email);
      alert("Password reset email sent! Check your inbox.");
      dispatch({ type: "TOGGLE_FORGOT_PASSWORD" });
      dispatch({ type: "TOGGLE_LOGIN_MODE" });
    } catch (err: any) {
      let errorMessage =
        "Failed to send password reset email. Please try again later.";
      if (err.code === "auth/invalid-email") {
        errorMessage = "Invalid email address. Please enter a valid email.";
      } else if (err.code === "auth/user-not-found") {
        errorMessage = "No user found with this email address.";
      }
      dispatch({ type: "SET_ERROR", payload: errorMessage });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  };

  return (
    <div className="login">
      <h1>Welcome to MLB Match Maker!</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <label>Email:</label>
        <input type="text" ref={userRef} disabled={state.isLoading} />
        {!state.forgotPassword ? (
          <>
            <label>Password:</label>
            <input type="password" ref={pwRef} disabled={state.isLoading} />
          </>
        ) : null}
      </form>
      {state.error && <div style={{ color: "red" }}>{state.error}</div>}
      {state.resend && (
        <span
          onClick={handleResendVerification}
          style={{
            cursor: "pointer",
            fontSize: ".8rem",
            textDecoration: "underline",
            marginTop: "10px",
          }}
        >
          Resend Verification Email
        </span>
      )}
      {state.forgotPassword ? (
        <Button onClick={handlePasswordReset}>
          {state.isLoading ? <Spinner size={30} /> : "Submit"}
        </Button>
      ) : (
        <Button
          onClick={state.isLogin ? handleLoginSubmit : handleSignupSubmit}
        >
          {state.isLoading ? <Spinner size={30} /> : "Submit"}
        </Button>
      )}

      <p>
        {state.isLogin ? (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <span
              onClick={() => dispatch({ type: "TOGGLE_LOGIN_MODE" })}
              style={{
                cursor: "pointer",
                fontSize: ".8rem",
                textDecoration: "underline",
                marginBottom: "15px",
              }}
            >
              Don't have an account? Sign up
            </span>
            {!state.forgotPassword ? (
              <span
                onClick={() => dispatch({ type: "TOGGLE_FORGOT_PASSWORD" })}
                style={{
                  cursor: "pointer",
                  fontSize: ".8rem",
                  textDecoration: "underline",
                }}
              >
                Forgot password
              </span>
            ) : (
              <span
                onClick={() => dispatch({ type: "TOGGLE_FORGOT_PASSWORD" })}
                style={{
                  cursor: "pointer",
                  fontSize: ".8rem",
                  textDecoration: "underline",
                }}
              >
                Go back
              </span>
            )}
          </div>
        ) : (
          <span
            onClick={() => dispatch({ type: "TOGGLE_LOGIN_MODE" })}
            style={{
              cursor: "pointer",
              fontSize: ".8rem",
              textDecoration: "underline",
            }}
          >
            Have an account? Login
          </span>
        )}
      </p>
    </div>
  );
}

export default Login;
