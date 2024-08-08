import { execFile } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name in an ES module context
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ApiController = {
  getTopBatters: (req, res) => {
    const scriptPath = path.join(__dirname, '../scraper/scraper.py');

    const pythonPath = path.join(__dirname, '../scraper/venv/bin/python3');

    const clearCache = req.query.clear === 'true' ? 'true' : 'false';


    // Execute the Python script
    execFile(pythonPath, [scriptPath, clearCache], (error, stdout, stderr) => {
      if (error) {
        console.error('Error executing Python script:', error);
        return res.status(500).send('Internal Server Error');
      }

      if (stderr) {
        console.error('Error output from Python script:', stderr);
        return res.status(500).send('Internal Server Error');
      }

      try {
        // Parse the output from Python script
        const data = JSON.parse(stdout);
        return res.status(200).json(data);
      } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
        return res.status(500).send('Internal Server Error');
      }
    });
  },
};

export default ApiController;
