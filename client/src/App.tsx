import React, { useState, useEffect } from "react";
import "./App.css";
import BatterTable from "./components/BatterTable";

interface Team {
  name: string;
  golfer: string;
  score: number | string;
}

function App() {
  const [data, setData] = useState([]);
  const [clearData, setClearData] = useState(false);

  const fetchLeaderboard = async () => {
    try {
      const response = await fetch(
        "http://localhost:3001/api/scraper?clear=" + clearData
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // console.log(response)
      const data = await response.json();
      console.log("data", data);

      setData(data);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <div className="App">
      <header className="header">
        <h1>Top Batters to Bet On Today</h1>
        <label>
          Clear Previous Data
          <input
            type="checkbox"
            checked={clearData}
            onChange={(e) => setClearData(!clearData)}
          />
        </label>

        <button onClick={fetchLeaderboard}>
          {data.length === 0 ? "Loading..." : "Refresh Data"}
        </button>
        <div className="Leaderboard-table">
          <BatterTable data={data}/>
        </div>
      </header>
    </div>
  );
}

export default App;
