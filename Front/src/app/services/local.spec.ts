import { TestBed } from '@angular/core/testing';

import { Local } from './local';

describe('Local', () => {
  let service: Local;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Local);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
