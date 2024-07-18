import express from 'express';
import cors from "cors";
import router from "./router.js";
const app = express();
const PORT = process.env.PORT || 3000;

const corsOptions = {
  origin: "https://golf-maker.vercel.app", // your frontend domain
  optionsSuccessStatus: 200,
};

app.use(express.json());
app.use(cors(corsOptions));
app.use("/api", router);

// Handles global errors v
app.use((err, req, res, next) => {
  res.status(500).json({ message: err.message });
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});