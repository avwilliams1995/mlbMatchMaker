import { execFile } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ApiController = {
  getTopBatters: (req, res) => {
    console.log("in scraper");
    const getTomorrow = req.query.tomorrow === "true";
    const targetDate = new Date();
    if (getTomorrow) targetDate.setDate(targetDate.getDate() + 1);
    const dateStr = targetDate.toISOString().slice(0, 10);
    console.log(`[scraper] getTomorrow=${getTomorrow}, pulling data for date ${dateStr}`);
    const scriptPath = path.join(__dirname, "../scraper/scraper.py");
    const pythonPath = path.join(__dirname, "../scraper/venv/bin/python3");

    const clearCache = req.query.clear === "true" ? "true" : "false";
    console.log("clearCache:", clearCache);
    console.log("getTomorrow:", getTomorrow);

    // Execute the Python script directly with the correct Python interpreter
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
          return res.status(500).send(stderr);
        }

        try {
          // Parse the output from Python script
          const data = JSON.parse(stdout);
          console.log("finished data:", data);
          return res.status(200).json(data);
        } catch (parseError) {
          console.error("Error parsing JSON:", parseError);
          return res.status(500).send("Internal Server Error");
        }
      }
    );
  },
};

export default ApiController;
