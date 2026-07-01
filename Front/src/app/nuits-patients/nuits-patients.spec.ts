import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NuitsPatients } from './nuits-patients';

describe('NuitsPatients', () => {
  let component: NuitsPatients;
  let fixture: ComponentFixture<NuitsPatients>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NuitsPatients],
    }).compileComponents();

    fixture = TestBed.createComponent(NuitsPatients);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
