import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { LocalService } from '../services/local';
export const authGuard: CanActivateFn = () => {
  const local = inject(LocalService);
  const router = inject(Router);
  return local.estConnecte() ? true : router.createUrlTree(['/login']);
};
