import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NuitsPatient } from './nuits-patient';

describe('NuitsPatient', () => {
  let component: NuitsPatient;
  let fixture: ComponentFixture<NuitsPatient>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NuitsPatient],
    }).compileComponents();

    fixture = TestBed.createComponent(NuitsPatient);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
