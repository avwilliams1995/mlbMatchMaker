import { spawn } from "child_process";

const ApiController = {
  async fetchData(req, res, next) {
    console.log('in fetch data')
    try {
      const pythonProcess = spawn("python3", ["../scraper/golfScraper.py"]); // Replace with the correct path to your Python script

      let dataString = "";

      pythonProcess.stdout.on("data", (data) => {
        dataString += data.toString();
      });

      pythonProcess.stdout.on("end", () => {
        const result = JSON.parse(dataString);
        res.locals.data = result; // Storing the data in res.locals to be used by other middleware if needed
        return next();
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
      return next({
        err: "Error in fetchData controller",
      });
    }
  },
};

export default ApiController;
