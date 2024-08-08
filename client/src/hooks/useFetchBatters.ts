import React, {useState, useEffect} from 'react'

function useFetchBatters(clearData:boolean) {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")
  const [data, setData] = useState([])

  useEffect(()=> {
    const fetchBatters = async () => {
      setIsLoading(true)
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
      } finally {
        setIsLoading(false)
      }
    };
    fetchBatters()
  })
}

export default useFetchBatters