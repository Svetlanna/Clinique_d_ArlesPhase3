import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CpapDashboard } from './cpap-dashboard';

describe('CpapDashboard', () => {
  let component: CpapDashboard;
  let fixture: ComponentFixture<CpapDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CpapDashboard],
    }).compileComponents();

    fixture = TestBed.createComponent(CpapDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
