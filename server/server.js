import express from 'express';
import cors from "cors";
import router from "./router.js";
const app = express();
const PORT = process.env.PORT || 3001;



app.use(cors()); 
app.use(express.json());

app.use("/api", router);

// Handles global errors 
app.use((err, req, res, next) => {
  res.status(500).json({ message: err.message });
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});