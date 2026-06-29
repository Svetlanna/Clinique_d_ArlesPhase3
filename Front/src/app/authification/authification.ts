import { Component,signal } from '@angular/core';
import { Router } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth';


@Component({
  selector: 'app-authification',
  standalone: true,
  imports: [ReactiveFormsModule,CommonModule],
  templateUrl: './authification.html',
  styleUrl: './authification.css',
})


export class Authification {
    protected readonly title = signal('CliniquePlus');

  message: string = '';
  loginForm: FormGroup;

  user = signal<any | null>(null);

  constructor(private fb: FormBuilder, private authService: AuthService,private router: Router) {
    this.loginForm = this.fb.group({
      mail: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe({
        next: (reponse: any) => {
          this.user.set(reponse);
          this.router.navigate(['/dashboard']);
        },
        error: (erreur) => {
          this.message = 'Connexion refusée !';
        }
      });
    }
  }




}
