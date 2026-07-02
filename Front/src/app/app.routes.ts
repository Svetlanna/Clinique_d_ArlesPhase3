import { Routes } from '@angular/router';
import { Authification } from './authification/authification';
import { Dashboard } from './dashboard/dashboard';
import { Appareils } from './appareils/appareils';
import { Medecines } from './medecines/medecines';
import { NuitsPatients } from './nuits-patients/nuits-patients';
import { AdminComponent } from './admin/admin';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: Authification },

  // Routes protégées par le Guard
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: 'appareils', component: Appareils, canActivate: [authGuard] },
  { path: 'medecines', component: Medecines, canActivate: [authGuard] },
  { path: 'nuitspatients', component: NuitsPatients, canActivate: [authGuard] },
  { path: 'admin', component: AdminComponent, canActivate: [authGuard] },

  // Redirections
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' },
];

