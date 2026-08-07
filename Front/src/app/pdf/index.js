import express from 'express';
import 'dotenv/config';
import cors from 'cors';

// Importation des routes
import nuitRoutes from './routes/nuitRoutes.js';
import MedecinsRoute from './routes/MedecinsRoute.js';
import appareilRoutes from './routes/appareilRoutes.js';
import analytiqueRoutes from './routes/analytiqueRoutes.js';
import cpapRoutes from './routes/cpapRoutes.js';
import authRoutes from './routes/authRoutes.js';
import patientRoutes from './routes/patientRoutes.js';

const app = express();

// Middleware
app.use(cors({ origin: 'http://localhost:4200' }));
app.use(express.json());

// Routes API
app.use('/api/patient', patientRoutes);
app.use('/api/nuit', nuitRoutes);
app.use('/api/med', MedecinsRoute);
app.use('/api/appareil', appareilRoutes);
app.use('/api/analytique', analytiqueRoutes);
app.use('/api/cpap', cpapRoutes);

// Routes Authentification
app.use('/auth', authRoutes);

app.listen(3000, () => console.log(`Server running on http://localhost:3000`));