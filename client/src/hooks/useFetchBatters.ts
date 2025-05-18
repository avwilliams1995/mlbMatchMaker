import { useState, useEffect } from "react";

function useFetchBatters<T>(): {
  data: T[];
  error: null | string;
  isLoading: boolean;
  refetch: (
    clearData: boolean,
    getTomorrow: boolean,
    signal?: AbortSignal
  ) => void;
} {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<null | string>(null);
  const [data, setData] = useState<T[]>([]);
  const [initialFetch, setInitialFetch] = useState(true);

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
        const text = await response.text(); // read plain text error
        throw new Error(`Server error: ${response.status} - ${text}`);
      }

      const data: T[] = await response.json();
      setData(data);
    } catch (err: any) {
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
    if (!initialFetch) {
      fetchTopBatters(false, false, controller.signal);
    }
    setInitialFetch(false);

    return () => {
      controller.abort();
    };
  }, []);
  return { data, error, isLoading, refetch: fetchTopBatters };
}

export default useFetchBatters;
