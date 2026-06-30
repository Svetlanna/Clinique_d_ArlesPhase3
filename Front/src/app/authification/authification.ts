import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-authification',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './authification.html',
  styleUrl: './authification.css',
})
export class Authification {
  protected readonly title = signal('CliniquePlus');
  message: string = '';
  loginForm: FormGroup;
  user = signal<any | null>(null);

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {
    // authification.ts
    this.loginForm = this.fb.group({
      login: ['', [Validators.required, Validators.email]],
      mot_de_passe: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe({
        next: (reponse: any) => {
          const userData = reponse?.data ?? reponse;
          this.authService.currentUser.set(userData);
          const role = userData?.role;

          if (role === 'admin') {
            this.router.navigate(['/admin']);
          } else if (role === 'medecin') {
            this.router.navigate(['/dashboard']);
          } else if (role === 'operateur') {
            this.router.navigate(['/operateur']);
          } else {
            this.router.navigate(['/dashboard']);
          }
        },
        error: (erreur) => {
          console.log('Erreur complète :', erreur.error);
          this.message = 'Identifiants incorrects !';
        },
      });
    }
  }
}
