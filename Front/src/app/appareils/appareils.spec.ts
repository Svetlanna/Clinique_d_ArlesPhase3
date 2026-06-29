import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Appareils } from './appareils';

describe('Appareils', () => {
  let component: Appareils;
  let fixture: ComponentFixture<Appareils>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Appareils],
    }).compileComponents();

    fixture = TestBed.createComponent(Appareils);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
