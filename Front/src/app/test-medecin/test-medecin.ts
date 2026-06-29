import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from '../components/sidebar/sidebar';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-test-medecin',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './test-medecin.html',
  styleUrl: './test-medecin.css',
})
export class TestMedecin {
  private authService = inject(AuthService);
  user = this.authService.currentUser;
}
