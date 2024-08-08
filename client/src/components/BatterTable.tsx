import React from "react";

const BatterTable = ({ data }: any) => {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th>Batter Name</th>
          <th>Overall Avg</th>
          <th>Batter Last 15</th>
          <th>Pitcher Avg vs Hand</th>
          <th>Batter Avg vs Hand</th>
          <th>Avg vs Pitcher</th>
          <th>Hits</th>
          <th>AB</th>
          <th>2B</th>
          <th>HR</th>
          <th>Batter Prev Game Hits</th>
          <th>URL</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item: any, index: number) => (
          <tr key={index}>
            <td>{item.batter_name}</td>
            <td>{item.overall_avg}</td>
            <td>{item.last_15}</td>
            <td>{item.hand_avg}</td>
            <td>{item.vs_hand}</td>
            <td>{item.avg}</td>
            <td>{item.hits}</td>
            <td>{item.at_bats}</td>
            <td>{item["2b"]}</td>
            <td>{item.home_runs}</td>
            <td>{item.prevHits}</td>
            <td>
              <a href={item.game_url} target="_blank" rel="noopener noreferrer">
                Link
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default BatterTable;
