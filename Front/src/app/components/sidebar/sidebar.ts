import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class SidebarComponent {
  private authService = inject(AuthService);
  private router = inject(Router);
  protected readonly title = signal('CliniquePlus');

  user = this.authService.currentUser;

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
