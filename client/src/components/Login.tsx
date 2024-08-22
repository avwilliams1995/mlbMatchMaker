import React, { useRef, useState, useEffect } from "react";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendEmailVerification,
  sendPasswordResetEmail,
  setPersistence,
  browserLocalPersistence,
  signOut,
} from "firebase/auth";
import { auth } from "../firebase";
import "../styles/Login.css";
import Button from "./Button";
import Spinner from "./Spinner";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Login() {
  const userRef = useRef<HTMLInputElement | null>(null);
  const pwRef = useRef<HTMLInputElement | null>(null);
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resend, setResend] = useState(false);
  const [forgotPassword, setForgotPassword] = useState(false);
  const navigate = useNavigate();
  const { setCurrentUser } = useAuth(); 

  const handleLoginSubmit = async () => {
    setIsLoading(true);
    setError(null);
    setResend(false);
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
        setError("Please verify your email before logging in.");
        setResend(true);
      }
    } catch (err) {
      console.log(err);
      setError(
        "Failed to log in. Please check your credentials and try again."
      );
    } finally {
      setIsLoading(false);
    }
    return;
  };

  const handleSignupSubmit = async () => {
    setIsLoading(true);
    setError(null);
    const username = userRef.current?.value || "";
    const pw = pwRef.current?.value || "";

    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        username,
        pw
      );
      const user = userCredential.user;

      // Send email verification
      await sendEmailVerification(user);

      setIsLogin(true);
      alert(
        "Sign up successful! Please check your email to verify your account before logging in."
      );
    } catch (err: any) {
      console.log(err.code);
      if (err.code === "auth/invalid-email") {
        setError("Invalid email address. Please enter a valid email.");
      } else if (err.code === "auth/email-already-in-use") {
        setError(
          "This email is already in use. Please use a different email or log in."
        );
      } else if (err.code === "auth/weak-password") {
        setError("Password is too weak. Please enter a stronger password.");
      } else {
        setError(
          "Failed to sign up. Please check your credentials and try again."
        );
      }
    } finally {
      setIsLoading(false);
    }
    return;
  };

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
  };

  const toggleForgotPassword = () => {
    setForgotPassword(!forgotPassword);
  };

  const handleResendVerification = async () => {
    setError(null);
    if (auth.currentUser) {
      await sendEmailVerification(auth.currentUser);
      alert("Verification email sent! Please check your inbox.");
      setIsLogin(true);
      setResend(false);
    }
  };

  const handlePasswordReset = async () => {
    setError(null);
    const email = userRef.current?.value || "";

    try {
      await sendPasswordResetEmail(auth, email);
      alert("Password reset email sent! Check your inbox.");
      setForgotPassword(false);
      setIsLogin(true);
    } catch (err: any) {
      if (err.code === "auth/invalid-email") {
        setError("Invalid email address. Please enter a valid email.");
      } else if (err.code === "auth/user-not-found") {
        setError("No user found with this email address.");
      } else {
        setError(
          "Failed to send password reset email. Please try again later."
        );
      }
    } finally {
      setIsLoading(false); // Ensure loading state is reset
    }
  };

  return (
    <div className="login">
      <h1>Welcome to MLB Match Maker!</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <label>Email:</label>
        <input type="text" ref={userRef} disabled={isLoading} />
        {!forgotPassword ? (
          <>
            <label>Password:</label>
            <input type="password" ref={pwRef} disabled={isLoading} />
          </>
        ) : null}
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {resend && (
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
      {forgotPassword ? (
        <Button onClick={handlePasswordReset}>
          {isLoading ? <Spinner size={30} /> : "Submit"}
        </Button>
      ) : (
        <Button onClick={isLogin ? handleLoginSubmit : handleSignupSubmit}>
          {isLoading ? <Spinner size={30} /> : "Submit"}
        </Button>
      )}

      <p>
        {isLogin ? (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <span
              onClick={toggleAuthMode}
              style={{
                cursor: "pointer",
                fontSize: ".8rem",
                textDecoration: "underline",
                marginBottom: "15px",
              }}
            >
              Don't have an account? Sign up
            </span>
            {!forgotPassword ? (
              <span
                onClick={toggleForgotPassword}
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
                onClick={toggleForgotPassword}
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
            onClick={toggleAuthMode}
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
