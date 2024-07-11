import { Router } from "express";
import ApiController from "./controller.js";
const router = Router();

router.get("/dailyFetch", (req, res) => {
  res.status(200).send("hello");
});

router.post("/scraper", (req, res) => {
  res.status(200).send(req.body);
});


export default router;