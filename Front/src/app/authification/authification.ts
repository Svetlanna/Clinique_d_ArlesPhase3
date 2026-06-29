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
    this.loginForm = this.fb.group({
      // Renommé 'mail' en 'login' pour correspondre à la colonne SQL
      login: ['', [Validators.required,Validators.email]],
      password: ['', [Validators.required, Validators.minLength(3)]],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe({
        next: (reponse: any) => {
          // On accède à 'reponse.data' pour récupérer l'objet utilisateur
          if (reponse && reponse.data) {
            this.user.set(reponse.data);
            this.router.navigate(['/dashboard']);
          }
        },
        error: (erreur) => {
          this.message = 'Connexion refusée !';
        },
      });
    }
  }
}