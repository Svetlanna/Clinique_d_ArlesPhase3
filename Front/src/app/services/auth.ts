import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  // Centralized state
  currentUser = signal<any | null>(null);
  appareils = signal<any | null>(null);
  medecines = signal<any | null>(null);

  constructor(private http: HttpClient) {}

  login(data: any) {
    return this.http.post('http://localhost:3000/auth/login', data).pipe(
      tap((reponse: any) => {
        // Si votre API renvoie { status: 'success', data: {...} }
        this.currentUser.set(reponse.data);
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
    return this.currentUser() !== null;
  }
}
