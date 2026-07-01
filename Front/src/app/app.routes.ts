import { Routes } from '@angular/router';
import { Authification } from './authification/authification';
import { Dashboard } from './dashboard/dashboard';
import { Appareils } from './appareils/appareils';
import { Medecines } from './medecines/medecines';
import { NuitsPatient } from './nuits-patient/nuits-patient';

export const routes: Routes = [
  { path: 'login', component: Authification },
  { path: 'dashboard', component: Dashboard },
  { path: 'appareils', component: Appareils },
  { path: 'medecines', component: Medecines },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: '' },
  {path: 'Nuits Patients', component:NuitsPatient}
];
