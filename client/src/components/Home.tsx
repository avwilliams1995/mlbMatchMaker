import React, { useMemo, useState } from "react";
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
  console.log(data);

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
    const controller = new AbortController();
    if (getTomorrow && !isTomorrowData) {
      refetch(true, true, controller.signal);
      setIsTomorrowData(true);
    } else {
      refetch(true, false, controller.signal);
      setIsTomorrowData(false);
    }
    
  };

  const handleFilter = (query: string) => {
    setSearchQuery(query);
  };

  const filteredData = useMemo(() => {
    if (!data) return [];
    return data.filter((batter: any) => {
      if (
        batter.batter_name.toLowerCase().includes(searchQuery.toLowerCase())
      ) {
        return batter;
      }
    });
  }, [data, searchQuery]);

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
