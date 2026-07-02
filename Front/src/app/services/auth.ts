import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { LocalService } from './local';
import {Router} from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser = signal<any | null>(null);
  appareils = signal<any | null>(null);
  medecines = signal<any | null>(null);
  nuits = signal<any[]>([]);

  constructor(private http: HttpClient, private localService: LocalService, private router: Router) {
    const mail = localService.getToken('auth_token');
    const role = localService.getToken('auth_role');
    if (mail) {
      this.currentUser.set({ mail, role });
    }
  }

  login(data: any) {
    return this.http
      .post('http://localhost:3000/auth/login', data)
      .pipe(tap((user: any) => this.currentUser.set(user)));
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

  fetchNuits() {
    return this.http
      .get<any>('http://localhost:3000/api/nuit')
      .pipe(tap((reponse) => this.nuits.set(reponse.data)));
  }

  updateCommentaire(idNuit: number, commentaire: string) {
    return this.http
      .patch<any>(`http://localhost:3000/api/nuit/${idNuit}/commentaire`, { commentaire });
  }

  logout() {
    this.currentUser.set(null);
    this.router.navigate(['/'])
  }

  isLoggedIn(): boolean {
    return this.currentUser() !== null;
  }
}