import React, { useState } from "react";
import "./App.css";
import BatterTable from "./components/BatterTable";
import useFetchBatters from "./hooks/useFetchBatters";
import Spinner from "./components/Spinner";

function App() {
  const [clearData, setClearData] = useState(false);
  const [getTomorrow, setGetTomorrow] = useState(false);
  const [isTomorrowData, setIsTomorrowData] = useState(false);
  const { data, error, isLoading, refetch } = useFetchBatters();

  console.log(data, isLoading, error);
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

        <button onClick={handleRefresh}>
          {isLoading ? "Scraping new data..." : "Refresh Data"}
        </button>
        {isTomorrowData && !isLoading ? <p>Tomorrow's data:</p> : null}
        <div className="Leaderboard-table">
          {isLoading ? <Spinner /> : <BatterTable data={data} />}
        </div>
      </header>
    </div>
  );
}

export default App;
