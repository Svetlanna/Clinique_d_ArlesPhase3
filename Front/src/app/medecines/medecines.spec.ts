import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Medecines } from './medecines';

describe('Medecines', () => {
  let component: Medecines;
  let fixture: ComponentFixture<Medecines>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Medecines],
    }).compileComponents();

    fixture = TestBed.createComponent(Medecines);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
