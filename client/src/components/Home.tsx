import React, { useMemo, useState, useEffect } from "react";
import "../styles/Home.css";
import BatterTable from "./BatterTable";
import useFetch from "../hooks/useFetchBatters";
import Spinner from "./Spinner";
import Button from "./Button";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useAuth } from "../context/AuthContext";
import Searchbar from "./Searchbar";

function Home() {
  const [clearData, setClearData] = useState(false);
  const [getTomorrow, setGetTomorrow] = useState(false);
  const [isTomorrowData, setIsTomorrowData] = useState(false);
  const { data, error, isLoading, refetch } = useFetch();
  const [searchQuery, setSearchQuery] = useState("");
  const { currentUser } = useAuth();
  const [abortController, setAbortController] = useState<AbortController | null>(null);
  const [timer, setTimer] = useState(0);
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);
  const [showTimer, setShowTimer] = useState(false);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      window.location.href = "/login";
    } catch (error) {
      console.error("Error logging out: ", error);
    }
  };

  const handleRefresh = () => {
    if (abortController) {
      abortController.abort();
    }

    const controller = new AbortController();
    setAbortController(controller);

    setTimer(0);
    setShowTimer(true);

    const id = setInterval(() => {
      setTimer((prev) => prev + 1);
    }, 1000);
    setIntervalId(id);

    if (getTomorrow && !isTomorrowData) {
      refetch(true, true, controller.signal);
      setIsTomorrowData(true);
    } else {
      refetch(true, false, controller.signal);
      setIsTomorrowData(false);
    }
  };

  const handleCancel = () => {
    if (abortController) {
      abortController.abort();
      setAbortController(null);
    }

    if (intervalId) {
      clearInterval(intervalId);
      setIntervalId(null);
    }

    setTimer(0);
    setShowTimer(false);
  };

  const handleFilter = (query: string) => {
    setSearchQuery(query);
  };

  const filteredData = useMemo(() => {
    if (!data) return [];
    return data.filter((batter: any) =>
      batter.batter_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [data, searchQuery]);

  useEffect(() => {
    if (!isLoading && intervalId) {
      clearInterval(intervalId);
      setIntervalId(null);
      setTimer(0);
      setShowTimer(false);
    }
  }, [isLoading]);
  console.log("data", data);

  return (
    <div className="App">
      <header className="header">
        <h1>Top Batters</h1>
        <div id="boxes">
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
          <Button onClick={isLoading ? handleCancel : handleRefresh}>
            {isLoading ? "Cancel" : "Refresh Data"}
          </Button>
          <Button onClick={handleLogout}>Log Out</Button>
        </div>

        {showTimer && (
          <>
            <div style={{ width: "100%", backgroundColor: "#ddd", height: "14px", marginTop: "6px", borderRadius: "4px", margin: "10px 0" }}>
              <div
                style={{
                  width: `${Math.min(Math.floor(timer / 8.4) * 7, 100)}%`,
                  backgroundColor: "#4caf50",
                  height: "100%",
                  transition: "width 0.3s ease-in-out",
                  borderRadius: "4px"
                }}
              />
            </div>
          </>
      )}

        <Searchbar handleSearch={handleFilter} />
        {isTomorrowData && !isLoading ? <p>Tomorrow's data:</p> : null}
        <div className="Leaderboard-table">
          {isLoading ? <Spinner /> : <BatterTable data={filteredData} />}
        </div>
      </header>
    </div>
  );
}

export default Home;