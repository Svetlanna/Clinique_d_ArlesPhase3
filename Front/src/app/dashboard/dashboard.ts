import { Component, inject, signal } from '@angular/core';
import { JsonPipe } from '@angular/common';
import { AuthService } from '../services/auth';
import { Router } from '@angular/router';
import { SidebarComponent } from '../components/sidebar/sidebar';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [JsonPipe,SidebarComponent],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard {
  protected readonly title = signal('CliniquePlus');

  private authService = inject(AuthService);
  private router = inject(Router);

  user = this.authService.currentUser;

  constructor() {
    if (!this.authService.currentUser()) {
      this.router.navigate(['/login']);
    }
  }

  logout() {
    this.user.set(null);

    this.router.navigate(['/login']);
  }
}
