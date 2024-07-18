import { spawn } from "child_process";

const ApiController = {
  async fetchData(req, res, next) {
    console.log("in fetch data");
    try {
      const pythonProcess = spawn("python3", ["../scraper/golfScraper.py"]); // Adjust the path if necessary

      let dataString = "";

      pythonProcess.stdout.on("data", (data) => {
        console.log(`stdout data: ${data.toString()}`);
        dataString += data.toString();
      });

      pythonProcess.stdout.on("end", () => {
        try {
          // Log the entire dataString received
          console.log(`full dataString: ${dataString}`);

          // Remove any leading/trailing whitespace and non-JSON characters
          const jsonString = dataString.trim().replace(/^200\s*/, "");
          console.log(`cleaned jsonString: ${jsonString}`);

          // Parse the cleaned JSON string
          const result = JSON.parse(jsonString);
          console.log("parsed result", result);
          res.locals.data = result; // Storing the data in res.locals to be used by other middleware if needed
          return next();
        } catch (err) {
          console.error(`Error parsing JSON: ${err.message}`);
          return next({
            err: `Error parsing JSON: ${err.message}`,
          });
        }
      });

      pythonProcess.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        return next({
          err: `Error in fetchData controller: ${data.toString()}`,
        });
      });

      pythonProcess.on("close", (code) => {
        if (code !== 0) {
          console.error(`Python process exited with code ${code}`);
          return next({
            err: `Python process exited with code ${code}`,
          });
        }
      });
    } catch (error) {
      console.error(`Error in fetchData controller: ${error.message}`);
      return next({
        err: "Error in fetchData controller",
      });
    }
  },
};

export default ApiController;
