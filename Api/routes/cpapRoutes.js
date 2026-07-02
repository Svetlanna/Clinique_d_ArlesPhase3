import express from 'express';
import { getAllCpap } from '../controllers/cpapController.js';

 const router = express.Router();

 router.get('/',getAllCpap);

 export default router;
