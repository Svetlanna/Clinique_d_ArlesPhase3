import express from 'express';
// Corrected: Remove the duplicate 'getStats'
import { getNuitData, getStats } from "../controllers/nuitController.js";

const router = express.Router();

router.get('/:id/run', getNuitData);
router.get('/:id/stats', getStats);

export default router;