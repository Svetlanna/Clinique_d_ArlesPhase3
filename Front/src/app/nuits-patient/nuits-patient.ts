import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { SidebarComponent } from '../components/sidebar/sidebar';

@Component({
  selector: 'app-nuits-patient',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './nuits-patient.html',
  styleUrl: './nuits-patient.css',
})
export class NuitsPatient implements OnInit {
  private http = inject(HttpClient);
  nuits: any[] = [];

  ngOnInit() {
    this.http.get<any>('http://localhost:3000/api/nuit').subscribe({
      next: (res) => (this.nuits = res.data),
      error: (err) => console.error('API Error:', err),
    });
  }
}
