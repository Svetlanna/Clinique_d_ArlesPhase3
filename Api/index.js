import express from 'express';
import 'dotenv/config';
import cors from 'cors';
import nuitRoutes from './routes/nuitRoutes.js';
import MedecinsRoute from './routes/MedecinsRoute.js';
import appareilRoutes from './routes/appareilRoutes.js';
import authRoutes from './routes/authRoutes.js';

const app = express();

app.use(cors({ origin: 'http://localhost:4200' }));
app.use(express.json());

app.use('/api/nuit', nuitRoutes);
app.use('/api/med', MedecinsRoute);
app.use('/api/appareil', appareilRoutes);
app.use('/auth', authRoutes);

app.listen(3000, () => console.log(`Server running on http://localhost:3000`));