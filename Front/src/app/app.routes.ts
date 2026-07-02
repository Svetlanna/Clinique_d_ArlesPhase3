import { Routes } from '@angular/router';
import { Authification } from './authification/authification';
import { Dashboard } from './dashboard/dashboard';
import { Appareils } from './appareils/appareils';
import { Medecines } from './medecines/medecines';
import { authGuard } from './guards/auth.guard';
import { NuitsPatients } from './nuits-patients/nuits-patients';

export const routes: Routes = [
  { path: 'login', component: Authification },
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: 'appareils', component: Appareils, canActivate: [authGuard] },
  { path: 'medecines', component: Medecines, canActivate: [authGuard] },
  { path: 'nuitspatients', component: NuitsPatients, canActivate: [authGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: '' }
];