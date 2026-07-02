import express from 'express';
import { getNuitData, getStats, getAllNuits, updateCommentaire } from "../controllers/nuitController.js";

const router = express.Router();

router.get('/', getAllNuits);
router.get('/:id/run', getNuitData);
router.get('/:id/stats', getStats);
router.patch('/:id/commentaire', updateCommentaire);

export default router;