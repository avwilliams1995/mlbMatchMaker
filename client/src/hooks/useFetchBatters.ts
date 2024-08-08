import { useState, useEffect } from "react";

function useFetchBatters() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<null | string>(null);
  const [data, setData] = useState([]);

  const fetchTopBatters = async (
    clearData: boolean = false,
    getTomorrow: boolean = false
  ) => {
    setIsLoading(true);
    try {
      console.log("in fetch data");
      const response = await fetch(
        `http://localhost:3001/api/scraper?clear=${clearData}&tomorrow=${getTomorrow}`
      );
      if (!response.ok){
        console.log(response)
      }

      const data = await response.json();
      setData(data);
    } catch (err) {
      console.log("Error fetching top batters:" + err);
      setError("Error fetching top batters");
    } finally {
      setIsLoading(false);
    }
  };
  useEffect(() => {
    fetchTopBatters();
  }, []);
  return { data, error, isLoading, refetch: fetchTopBatters };
}

export default useFetchBatters;
