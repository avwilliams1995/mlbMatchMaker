import React, { useState, useEffect } from 'react';
import './App.css';

interface Team {
  name: string;
  golfer: string;
  score: number | string;
}

function App() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchLeaderboard = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:3000/api/scraper");
      const data = await response.json();
      console.log('data', data)

      const sortedData = data.sort((a: Team, b: Team) => {
        const scoreA = a.score === "E" ? 0 : Number(a.score);
        const scoreB = b.score === "E" ? 0 : Number(b.score);
        return scoreA - scoreB;
      });
      
      setTeams(sortedData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Travel League Golf Leaderboard</h1>
        <button onClick={fetchLeaderboard} disabled={loading}>
          {loading ? "Loading..." : "Refresh Leaderboard"}
        </button>
        <div className="Leaderboard-table-container">
          <table className="Leaderboard-table">
            <thead>
              <tr>
                <th>Team Name</th>
                <th>Golfer</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {teams.map((team, index) => (
                <tr key={index}>
                  <td>{team.name}</td>
                  <td>{team.golfer}</td>
                  <td>{team.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </header>
    </div>
  );
}

export default App;
