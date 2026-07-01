import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth';
import { SidebarComponent } from '../components/sidebar/sidebar';
import { DatePipe } from '@angular/common';


@Component({
  selector: 'app-medecines',
  standalone: true,
  // 2. Add Sidebar to the imports array
  imports: [DatePipe, CommonModule, RouterModule, SidebarComponent],
  templateUrl: './medecines.html',
  styleUrl: './medecines.css',
})
export class Medecines implements OnInit {
  private authService = inject(AuthService);
  medecines = this.authService.medecines;

  ngOnInit() {
    this.authService.fetchMedecines().subscribe({
      next: (res) => console.log('Data received:', res),
      error: (err) => console.error('API Error:', err),
    });
  }
}
