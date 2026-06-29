import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { LocalService } from './local';

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser = signal<any | null>(null);
  appareils = signal<any | null>(null);
  medecines = signal<any | null>(null);

  constructor(private http: HttpClient, private localService: LocalService) {
    const mail = localService.getToken('auth_token');
    const role = localService.getToken('auth_role');
    if (mail) {
      this.currentUser.set({ mail, role });
    }
  }

  login(data: any) {
    return this.http
      .post<any>('http://localhost:3000/auth/login', data)
      .pipe(
        tap((reponse) => {
          const { mail, password: role } = reponse.data;
          this.localService.login(mail);
          this.localService.saveToken('auth_role', role);
          this.currentUser.set({ mail, role });
        })
      );
  }

  getAppareils() {
    return this.http
      .get<any>('http://localhost:3000/api/appareil')
      .pipe(tap((reponse) => this.appareils.set(reponse.data)));
  }

  fetchMedecines() {
    return this.http
      .get<any>('http://localhost:3000/api/med')
      .pipe(tap((reponse) => this.medecines.set(reponse.data)));
  }

  logout() {
    this.currentUser.set(null);
    this.localService.logout();
  }

  isLoggedIn(): boolean {
    return this.localService.estConnecte();
  }
}
