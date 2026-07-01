import express from 'express';

import {medecineRoute, getMedecinById } from '../controllers/nuitController.js';

const router = express.Router();


router.get('/', medecineRoute);
router.get('/:id', getMedecinById);

export default router;


