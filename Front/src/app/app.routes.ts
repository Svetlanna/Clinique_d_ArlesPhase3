import { Routes } from '@angular/router';
import { Authification } from './authification/authification';
import { Dashboard } from './dashboard/dashboard';
import { Appareils } from './appareils/appareils';
import { Medecines } from './medecines/medecines';
import { TestMedecin } from './test-medecin/test-medecin';
import { TestOperateur } from './test-operateur/test-operateur';
import { ResultatsNuit } from './resultats-nuit/resultats-nuit';
import { NuitsPatients } from './nuits-patients/nuits-patients';
import { authGuard } from './guards/auth.guard';
import { roleGuard } from './guards/role.guard';

export const routes: Routes = [
  { path: 'login', component: Authification },
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: 'appareils', component: Appareils, canActivate: [authGuard] },
  { path: 'resultats-nuit', component: ResultatsNuit, canActivate: [authGuard] },
  { path: 'nuitspatients', component: NuitsPatients, canActivate: [authGuard] },
  { path: 'medecines', component: Medecines, canActivate: [authGuard, roleGuard(['medecin', 'admin'])] },
  { path: 'test-medecin', component: TestMedecin, canActivate: [authGuard, roleGuard(['medecin', 'admin'])] },
  { path: 'test-operateur', component: TestOperateur, canActivate: [authGuard, roleGuard(['operateur', 'admin'])] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: '' },
];