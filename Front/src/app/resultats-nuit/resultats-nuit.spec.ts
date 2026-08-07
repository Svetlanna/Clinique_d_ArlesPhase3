import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultatsNuit } from './resultats-nuit';

describe('ResultatsNuit', () => {
  let component: ResultatsNuit;
  let fixture: ComponentFixture<ResultatsNuit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResultatsNuit],
    }).compileComponents();

    fixture = TestBed.createComponent(ResultatsNuit);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
