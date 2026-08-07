import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { LocalService } from './local';

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser = signal<any | null>(null);
  appareils = signal<any | null>(null);
  medecines = signal<any | null>(null);
  nuits = signal<any[]>([]);
  patients = signal<any[]>([]);
  resultats = signal<any[]>([]);
  patientDetail = signal<any | null>(null);
  cpap = signal<any[]>([]);
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
    return this.http.post<any>('http://localhost:3000/auth/login', data).pipe(
      tap((res) => {
        const user = res.data;
        this.currentUser.set(user);
        this.localService.saveToken('auth_token', user.mail);
        this.localService.saveToken('auth_role', user.role);
      }),
    );
  }

  logout() {
    this.currentUser.set(null);
    this.localService.removeToken('auth_token');
    this.localService.removeToken('auth_role');
  }

  isLoggedIn(): boolean {
    return this.currentUser() !== null;
  }

  getAppareils() {
    return this.http
      .get<any>('http://localhost:3000/api/appareil')
      .pipe(tap((reponse) => this.appareils.set(reponse.data)));
  }
  fetchCpap() {
    return this.http
      .get<any>('http://localhost:3000/api/cpap')
      .pipe(tap((reponse) => this.cpap.set(reponse.cpap)));
  }

  fetchMedecines() {
    return this.http
      .get<any>('http://localhost:3000/api/med')
      .pipe(tap((reponse) => this.medecines.set(reponse.data)));
  }

  fetchNuits() {
    return this.http.get<any>('http://localhost:3000/api/nuit/all').pipe(
      tap((reponse) => {
        this.nuits.set([]);
        this.nuits.set(reponse.data);
      }),
    );
  }
  updateMedecin(idNuit: number, idMedecin: number) {
    return this.http.patch<any>(`http://localhost:3000/api/nuit/${idNuit}/medecin`, { idMedecin });
  }

  updateCommentaire(idNuit: number, commentaire: string) {
    return this.http.patch<any>(`http://localhost:3000/api/nuit/${idNuit}/commentaire`, {
      commentaire,
    });
  }

  fetchPatients() {
    return this.http
      .get<any>('http://localhost:3000/api/patient')
      .pipe(tap((reponse) => this.patients.set(reponse.data)));
  }

  fetchPatientDetail(idPatient: number | string) {
    return this.http
      .get<any>(`http://localhost:3000/api/patient/${idPatient}`)
      .pipe(tap((reponse) => this.patientDetail.set(reponse.data)));
  }

  fetchResultats(idPatient: number | string) {
    return this.http
      .get<any>(`http://localhost:3000/api/patient/${idPatient}/resultats`)
      .pipe(tap((reponse) => this.resultats.set(reponse.data)));
  }
}
