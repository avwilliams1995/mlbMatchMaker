import { useState, useEffect } from "react";

function useFetchBatters() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<null | string>(null);
  const [data, setData] = useState([]);

  const fetchTopBatters = async (
    clearData: boolean = false,
    getTomorrow: boolean = false,
    signal?: AbortSignal
  ) => {
    setIsLoading(true);

    const controller = signal ? null : new AbortController();
    const effectiveSignal = signal || controller?.signal;

    try {
      console.log("in fetch data");
      const response = await fetch(
        `http://localhost:3001/api/scraper?clear=${clearData}&tomorrow=${getTomorrow}`,
        { signal: effectiveSignal }
      );
      if (!response.ok) {
        console.log(response);
      }

      const data = await response.json();
      setData(data);
    } catch (err:any) {
      if (err.name === "AbortError") {
        console.log("Fetch aborted"); 
        return;
      }
      console.log("Error fetching top batters:" + err);
      setError("Error fetching top batters");
    } finally {
      setIsLoading(false);
    }
  };
  useEffect(() => {
    const controller = new AbortController();
    fetchTopBatters(false, false, controller.signal);

    return () => {
      controller.abort();
    };
  }, []);
  return { data, error, isLoading, refetch: fetchTopBatters };
}

export default useFetchBatters;
