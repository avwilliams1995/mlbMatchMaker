import { Router } from "express";
import ApiController from "./controller.js";

const router = Router();

router.get("/dailyFetch", (req, res) => {
  res.status(200).send("hello");
});

router.get("/scraper", ApiController.fetchData, (req, res) => {
  res.status(200).json(res.locals.data); // Ensuring JSON response
});

export default router;
