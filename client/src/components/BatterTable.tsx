import React from 'react';

const BatterTable = ({ data }:any) => {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          <th>Batter Name</th>
          <th>Overall Avg</th>
          <th>Hand Avg</th>
          <th>vs Hand</th>
          <th>Last 15</th>
          <th>Avg</th>
          <th>Hits</th>
          <th>At Bats</th>
          <th>2B</th>
          <th>HR</th>
          <th>Prev Hits</th>
          <th>Game URL</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item:any, index:number) => (
          <tr key={index}>
            <td>{item.batter_name}</td>
            <td>{item.overall_avg}</td>
            <td>{item.hand_avg}</td>
            <td>{item.vs_hand}</td>
            <td>{item.last_15}</td>
            <td>{item.avg}</td>
            <td>{item.hits}</td>
            <td>{item.at_bats}</td>
            <td>{item['2b']}</td>
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