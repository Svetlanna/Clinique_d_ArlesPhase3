import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { LocalService } from './local';

@Injectable({ providedIn: 'root' })
export class AuthService {
  // Centralized state
  currentUser = signal<any | null>(null);
  appareils = signal<any | null>(null);
  medecines = signal<any | null>(null);

  constructor(
    private http: HttpClient,
    private localService: LocalService,
  ) {
    const mail = localService.getToken('auth_token');
    const role = localService.getToken('auth_role');
    if (mail) {
      this.currentUser.set({ mail, role });
    }
  }
  login(data: any) {
    // ← mapping obligatoire ici
    const payload = {
      login: data.login,
      password: data.mot_de_passe,
    };

    console.log('Payload envoyé:', payload); // vérifie dans la console

    return this.http.post<any>('http://localhost:3000/auth/login', payload).pipe(
      tap((reponse) => {
        const userData = reponse.data;
        this.localService.login(userData.login);
        this.localService.saveToken('auth_role', userData.role);
        this.currentUser.set(userData);
      }),
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
  }

  isLoggedIn(): boolean {
    return this.localService.estConnecte();
  }
}
