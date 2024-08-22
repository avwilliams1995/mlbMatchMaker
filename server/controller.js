import { execFile, exec } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ApiController = {
  getTopBatters: (req, res) => {
    console.log("in scraper");
    const scriptPath = path.join(__dirname, "../scraper/scraper.py");
    const pythonPath = path.join(__dirname, "../scraper/venv/bin/python3");
    const pipPath = path.join(__dirname, "../scraper/venv/bin/pip");

    const clearCache = req.query.clear === "true" ? "true" : "false";
    const getTomorrow = req.query.tomorrow === "true" ? "true" : "false";

    // Install dependencies first
    exec(
      `${pipPath} install -r ${path.join(
        __dirname,
        "../scraper/requirements.txt"
      )}`,
      (pipError, pipStdout, pipStderr) => {
        if (pipError) {
          console.error("Error installing dependencies:", pipError);
          return res.status(500).send("Internal Server Error");
        }

        if (pipStderr) {
          console.error("Error output from pip:", pipStderr);
          return res.status(500).send("Internal Server Error");
        }

        // Execute the Python script after installing dependencies
        execFile(
          pythonPath,
          [scriptPath, clearCache, getTomorrow],
          (error, stdout, stderr) => {
            if (error) {
              console.error("Error executing Python script:", error);
              return res.status(500).send("Internal Server Error");
            }

            if (stderr) {
              console.error("Error output from Python script:", stderr);
              return res.status(500).send("Internal Server Error");
            }

            try {
              // Parse the output from Python script
              const data = JSON.parse(stdout);
              return res.status(200).json(data);
            } catch (parseError) {
              console.error("Error parsing JSON:", parseError);
              return res.status(500).send("Internal Server Error");
            }
          }
        );
      }
    );
  },
};

export default ApiController;
