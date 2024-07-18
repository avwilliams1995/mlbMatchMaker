import express from "express";
import cors from "cors";
import path from "path";
import router from "./router.js";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(cors({ origin: "*" }));
app.use("/api", router);

// Serve static files from the React app
app.use(express.static(path.join(__dirname, "..", "client", "build")));

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "..", "client", "build", "index.html"));
});

// Handles global errors
app.use((err, req, res, next) => {
  res.status(500).json({ message: err.message });
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
