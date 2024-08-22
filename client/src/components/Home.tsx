import React, { useState } from "react";
import "../styles/Home.css";
import BatterTable from "./BatterTable";
import useFetchBatters from "../hooks/useFetchBatters";
import Spinner from "./Spinner";
import Button from "./Button";
import { signOut } from "firebase/auth";
import { auth } from "../firebase"; 
import { useAuth } from "../context/AuthContext";

function Home() {
  const [clearData, setClearData] = useState(false);
  const [getTomorrow, setGetTomorrow] = useState(false);
  const [isTomorrowData, setIsTomorrowData] = useState(false);
  const { data, error, isLoading, refetch } = useFetchBatters();
  const {currentUser} = useAuth();


  const handleLogout = async () => {
    try {
      await signOut(auth);
      window.location.href = "/login"; 
    } catch (error) {
      console.error("Error logging out: ", error);
    }
  };

  const handleRefresh = () => {
    console.log("in handle refresh");
    if (getTomorrow && !isTomorrowData) {
      refetch(true, true);
      setIsTomorrowData(true);
    } else {
      refetch(true, false);
      setIsTomorrowData(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Top Batters</h1>
        <div id="boxes">
          <label>
            Clear Previous Data
            <input
              type="checkbox"
              checked={clearData}
              onChange={(e) => setClearData(e.target.checked)}
            />
          </label>
          <label>
            Get Tomorrow's Data?
            <input
              type="checkbox"
              checked={getTomorrow}
              onChange={(e) => setGetTomorrow(e.target.checked)}
            />
          </label>
        </div>
        <div id="buttons">
          <Button onClick={handleRefresh}>
            {isLoading ? "Scraping new data..." : "Refresh Data"}
          </Button>
          <Button onClick={handleLogout}>Log Out</Button>
        </div>
        {isTomorrowData && !isLoading ? <p>Tomorrow's data:</p> : null}
        <div className="Leaderboard-table">
          {isLoading ? <Spinner /> : <BatterTable data={data} />}
        </div>
      </header>
    </div>
  );
}

export default Home;
