import { Router } from "express";
import ApiController from "./controller.js";
const router = Router();

router.get("/dailyFetch", (req, res) => {
  res.status(200).send("hello");
});

router.get("/scraper", ApiController.getTopBatters, (req, res) => {
  res.status(200).send(res.locals.data);
});

export default router;
