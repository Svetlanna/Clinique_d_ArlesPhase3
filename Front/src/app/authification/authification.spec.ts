import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Authification } from './authification';

describe('Authification', () => {
  let component: Authification;
  let fixture: ComponentFixture<Authification>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Authification],
    }).compileComponents();

    fixture = TestBed.createComponent(Authification);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
